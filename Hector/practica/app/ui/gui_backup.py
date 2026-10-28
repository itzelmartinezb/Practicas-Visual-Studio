import json, threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from app.config import settings
from app.db.mongo import MongoDB
from app.repositories.repository import Repository
from app.services.rules_engine import evaluar_camion, tabla_verdad
from app.services.llm_service import LLMService
from app.services.classifier import hybrid_classify
from app.services.reports import export_json, export_csv, export_pdf

COLLECTIONS=["camiones","accesos","incidentes","riesgos_eticos","evaluaciones_llm"]

class LogiSmartGUI(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("LogiSmart - Sistema híbrido LLM"); self.geometry("1250x800")
        self.db=MongoDB(settings.mongodb_uri,settings.database); self.repo=Repository(self.db)
        self.llm=LLMService(settings.ollama_host,settings.ollama_model,settings.llm_timeout)
        self.status=tk.StringVar(value="Conectando...")
        self._style(); self._build(); self._connect()

    def _style(self):
        s=ttk.Style(self); s.theme_use("clam")
        s.configure("Title.TLabel",font=("Segoe UI",18,"bold")); s.configure("Treeview",rowheight=28)

    def _build(self):
        top=ttk.Frame(self,padding=10); top.pack(fill="x"); ttk.Label(top,text="LOGISMART",style="Title.TLabel").pack(side="left"); ttk.Label(top,textvariable=self.status).pack(side="right")
        self.nb=ttk.Notebook(self); self.nb.pack(fill="both",expand=True,padx=10,pady=5)
        self._dashboard(); self._access(); self._truth(); self._incidents(); self._assistant(); self._risks(); self._crud(); self._reports(); self._config()

    def _connect(self):
        ok,msg=self.db.connect(); self.status.set(msg); 
        if not ok: messagebox.showwarning("MongoDB",msg+"\nPuedes iniciar en modo simulación, pero las funciones persistentes estarán limitadas.")
        self.refresh_all()

    def _tab(self,name):
        f=ttk.Frame(self.nb,padding=10); self.nb.add(f,text=name); return f

    def _dashboard(self):
        f=self._tab("Panel"); self.dash=ttk.Label(f,text="Cargando..."); self.dash.pack(anchor="nw")
        ttk.Button(f,text="Actualizar",command=self.refresh_dashboard).pack(anchor="nw",pady=10)

    def refresh_dashboard(self):
        try:
            c=len(self.repo.list("camiones")); i=len([x for x in self.repo.list("incidentes") if x.get("estado")!="cerrado"]); r=0
            for x in self.repo.list("riesgos_eticos"):
                if x.get("riesgo_residual",x.get("puntaje_residual",0))>=12: r+=1
            self.dash.config(text=f"Camiones atendidos: {c}\nIncidentes abiertos: {i}\nRiesgos críticos: {r}\nFecha: {datetime.now():%Y-%m-%d %H:%M}")
        except Exception as e:self.dash.config(text=f"Error: {e}")

    def _access(self):
        f=self._tab("Control de acceso"); left=ttk.Frame(f); left.pack(side="left",fill="y",padx=10)
        self.vars={k:tk.BooleanVar() for k in "PQRS"}; labels={"P":"Autorización","Q":"Peso excedido","R":"Material peligroso","S":"Certificación vigente"}
        for k in "PQRS": ttk.Checkbutton(left,text=f"{k} - {labels[k]}",variable=self.vars[k]).pack(anchor="w",pady=4)
        self.cert=tk.BooleanVar(value=True); self.hor=tk.BooleanVar(value=True)
        ttk.Checkbutton(left,text="V - Certificación vigente",variable=self.cert).pack(anchor="w"); ttk.Checkbutton(left,text="H - Horario seguro",variable=self.hor).pack(anchor="w")
        ttk.Button(left,text="Evaluar",command=self.evaluate_access).pack(pady=12)
        self.access_out=tk.Text(f,width=80,height=22); self.access_out.pack(side="left",fill="both",expand=True)

    def evaluate_access(self):
        d=evaluar_camion(*(self.vars[k].get() for k in "PQRS"),self.cert.get(),self.hor.get()); self.access_out.delete("1.0","end"); self.access_out.insert("end",json.dumps(d,ensure_ascii=False,indent=2))
        try:
            d2=dict(d); d2["marca_tiempo"]=datetime.now(); d2["operador"]="GUI"; self.db.create("accesos",d2)
        except Exception: pass

    def _truth(self):
        f=self._tab("Tablas de verdad"); self.truth=ttk.Treeview(f,columns=["P","Q","R","S","V","H","A","E","ACCESO"],show="headings")
        for c in self.truth["columns"]: self.truth.heading(c,text=c); self.truth.column(c,width=75,anchor="center")
        self.truth.pack(fill="both",expand=True); self.refresh_truth()
    def refresh_truth(self):
        for x in self.truth.get_children(): self.truth.delete(x)
        for r in tabla_verdad(): self.truth.insert("","end",values=[int(r[k]) for k in self.truth["columns"]])

    def _incidents(self):
        f=self._tab("Incidentes"); self.mail=tk.Text(f,height=8); self.mail.pack(fill="x"); bar=ttk.Frame(f); bar.pack(fill="x",pady=5)
        ttk.Button(bar,text="Clasificar híbrido",command=self.classify_incident).pack(side="left"); ttk.Button(bar,text="Limpiar",command=lambda:self.mail.delete("1.0","end")).pack(side="left",padx=5)
        self.inc_out=tk.Text(f,height=12); self.inc_out.pack(fill="both",expand=True)
        ttk.Label(f,text="Estado: nuevo / en_atencion / cerrado. El resultado puede editarse antes de guardar.").pack(anchor="w")
    def classify_incident(self):
        text=self.mail.get("1.0","end").strip()
        if not text:return messagebox.showwarning("Validación","Pega un correo primero.")
        self.inc_out.insert("end","Procesando LLM...\n"); self.update_idletasks()
        def work():
            final,meta=hybrid_classify(text,self.llm)
            self.after(0,lambda:self._finish_inc(text,final,meta))
        threading.Thread(target=work,daemon=True).start()
    def _finish_inc(self,text,final,meta):
        self.inc_out.delete("1.0","end"); self.inc_out.insert("end",json.dumps({"clasificacion":final,"metadatos":meta},ensure_ascii=False,indent=2))
        try:
            self.db.create("incidentes",{"correo_original":text,"clasificacion":final,"datos_extraidos":meta,"estado":"nuevo","fecha":datetime.now()})
            self.db.create("evaluaciones_llm",{"prompt":text,"respuesta":final,"modelo":settings.ollama_model,"latencia":meta.get("latencia"),"coincidio_reglas":not meta.get("requiere_revision_humana",True),"fecha":datetime.now()})
        except Exception as e:self.status.set(str(e))

    def _assistant(self):
        f=self._tab("Asistente RAG"); self.chat=tk.Text(f); self.chat.pack(fill="both",expand=True); b=ttk.Frame(f); b.pack(fill="x"); self.q=tk.Entry(b); self.q.pack(side="left",fill="x",expand=True); self.q.bind("<Return>",lambda e:self.ask()); ttk.Button(b,text="Preguntar",command=self.ask).pack(side="left")
    def ask(self):
        q=self.q.get().strip(); self.q.delete(0,"end")
        if not q:return
        self.chat.insert("end",f"\nOperador: {q}\nAsistente: consultando MongoDB...\n"); self.update_idletasks()
        try:
            terms=q.upper().split(); ctx=[]
            for t in terms:
                if t.startswith("CAM") or t.startswith("TRK"):
                    ctx += self.db.find("accesos",{"placa":t},10)
            if not ctx: ctx=self.db.find("accesos",{},10) if any(x in q.lower() for x in ["acceso","inspección","inspeccion"]) else []
            ans=self.llm.explain(q,ctx); self.chat.insert("end",ans+"\n")
        except Exception as e:self.chat.insert("end",f"Error: {e}\n")

    def _risks(self):
        f=self._tab("Riesgos éticos"); self.risk_tree=ttk.Treeview(f,columns=("modulo","categoria","prob","impacto","residual","mitigacion"),show="headings")
        for c in self.risk_tree["columns"]: self.risk_tree.heading(c,text=c.title())
        self.risk_tree.pack(fill="both",expand=True); bar=ttk.Frame(f); bar.pack(fill="x",pady=5)
        ttk.Button(bar,text="Actualizar",command=self.refresh_risks).pack(side="left"); ttk.Button(bar,text="Gráfica",command=self.risk_chart).pack(side="left",padx=5); ttk.Button(bar,text="Editar/alta/baja en CRUD",command=lambda:self.nb.select(6)).pack(side="left")
        self.refresh_risks()
    def refresh_risks(self):
        for x in self.risk_tree.get_children():self.risk_tree.delete(x)
        try:
            for r in self.repo.list("riesgos_eticos"):
                self.risk_tree.insert("","end",values=(r.get("modulo"),r.get("categoria"),r.get("probabilidad"),r.get("impacto"),r.get("riesgo_residual",r.get("puntaje_residual","-")),r.get("mitigacion")))
        except: pass

    def risk_chart(self):
        try:
            import matplotlib.pyplot as plt
            from collections import Counter
            data=self.repo.list("riesgos_eticos"); counts=Counter(r.get("categoria","sin_categoria") for r in data)
            if not counts: return messagebox.showinfo("Riesgos","No hay riesgos registrados.")
            plt.figure(figsize=(8,4)); plt.bar(list(counts),list(counts.values())); plt.title("Riesgos éticos por categoría"); plt.ylabel("Cantidad"); plt.xticks(rotation=25); plt.tight_layout(); plt.show()
        except Exception as e: messagebox.showerror("Gráfica",str(e))

    def _crud(self):
        f=self._tab("CRUD MongoDB"); top=ttk.Frame(f); top.pack(fill="x"); self.col=tk.StringVar(value="camiones"); ttk.Combobox(top,textvariable=self.col,values=COLLECTIONS,state="readonly").pack(side="left"); ttk.Button(top,text="Consultar",command=self.load_crud).pack(side="left",padx=5); ttk.Button(top,text="Nuevo JSON",command=self.new_doc).pack(side="left")
        self.crud=ttk.Treeview(f,columns=("id","json"),show="headings"); self.crud.heading("id",text="_id"); self.crud.heading("json",text="Documento"); self.crud.pack(fill="both",expand=True); self.crud.bind("<Double-1>",self.edit_doc)
    def load_crud(self):
        for x in self.crud.get_children():self.crud.delete(x)
        try:
            for d in self.repo.list(self.col.get()):
                ident=str(d.pop("_id", "")); self.crud.insert("","end",iid=ident,values=(ident,json.dumps(d,default=str,ensure_ascii=False)))
        except Exception as e: messagebox.showerror("MongoDB",str(e))
    def new_doc(self):
        w=tk.Toplevel(self); w.title("Nuevo documento"); t=tk.Text(w,width=90,height=25); t.pack(); ttk.Button(w,text="Guardar",command=lambda:self._save_new(w,t)).pack()
    def _save_new(self,w,t):
        try:self.repo.create(self.col.get(),json.loads(t.get("1.0","end"))); w.destroy(); self.load_crud()
        except Exception as e:messagebox.showerror("Error",str(e))
    def edit_doc(self,e):
        item=self.crud.selection()[0]; old=json.loads(self.crud.item(item,"values")[1]); w=tk.Toplevel(self); t=tk.Text(w,width=90,height=25); t.insert("1.0",json.dumps(old,ensure_ascii=False,indent=2)); t.pack(); ttk.Button(w,text="Actualizar",command=lambda:self._update_doc(w,t,item)).pack(); ttk.Button(w,text="Eliminar",command=lambda:self._delete_doc(w,item)).pack()
    def _update_doc(self,w,t,i):
        try:self.repo.update(self.col.get(),i,json.loads(t.get("1.0","end"))); w.destroy(); self.load_crud()
        except Exception as e:messagebox.showerror("Error",str(e))
    def _delete_doc(self,w,i):
        if messagebox.askyesno("Confirmar","¿Eliminar documento?"): self.repo.delete(self.col.get(),i); w.destroy(); self.load_crud()

    def _reports(self):
        f=self._tab("Reportes"); ttk.Button(f,text="Exportar colección a JSON",command=self.report_json).pack(anchor="w",pady=5); ttk.Button(f,text="Exportar colección a CSV",command=self.report_csv).pack(anchor="w",pady=5); ttk.Button(f,text="Exportar resumen PDF",command=self.report_pdf).pack(anchor="w",pady=5); ttk.Button(f,text="Agregación incidentes por categoría/semana",command=self.aggregation).pack(anchor="w",pady=5)
    def report_json(self):
        p=filedialog.asksaveasfilename(defaultextension=".json");
        if p: export_json(p,self.repo.list(self.col.get()))
    def report_csv(self):
        p=filedialog.asksaveasfilename(defaultextension=".csv");
        if p: export_csv(p,self.repo.list(self.col.get()))
    def report_pdf(self):
        p=filedialog.asksaveasfilename(defaultextension=".pdf");
        if p: export_pdf(p,"Reporte LogiSmart",[json.dumps(x,default=str,ensure_ascii=False) for x in self.repo.list(self.col.get())])
    def aggregation(self):
        try: messagebox.showinfo("Agregación",json.dumps(self.db.incident_week_aggregation(),default=str,ensure_ascii=False,indent=2))
        except Exception as e:messagebox.showerror("MongoDB",str(e))

    def _config(self):
        f=self._tab("Configuración")
        ttk.Label(f,text="Modelo Ollama:").grid(row=0,column=0,sticky="w",pady=6); self.model_var=tk.StringVar(value=settings.ollama_model); ttk.Entry(f,textvariable=self.model_var,width=40).grid(row=0,column=1,sticky="w")
        ttk.Label(f,text="Host Ollama:").grid(row=1,column=0,sticky="w",pady=6); self.host_var=tk.StringVar(value=settings.ollama_host); ttk.Entry(f,textvariable=self.host_var,width=40).grid(row=1,column=1,sticky="w")
        self.sim_var=tk.BooleanVar(value=settings.simulation_mode); ttk.Checkbutton(f,text="Modo simulación de correo",variable=self.sim_var).grid(row=2,column=0,columnspan=2,sticky="w",pady=6)
        ttk.Label(f,text="Los cambios se aplican al reiniciar para evitar modificar procesos LLM activos.").grid(row=3,column=0,columnspan=2,sticky="w",pady=10)

    def new_doc_from_data(self,*a): pass
    def refresh_all(self): self.refresh_dashboard(); self.refresh_risks()

if __name__=="__main__": LogiSmartGUI().mainloop()
