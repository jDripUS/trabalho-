import argparse
import importlib
import subprocess
import sys
from pathlib import Path

def ensure_dependencies(req_path: Path):
    try:
        import pandas  # quick check
        import pydantic  # quick check
    except Exception:
        print("Dependências faltando — instalando a partir de", req_path)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_path)])

def choose_paths_via_gui():
    # GUI import local (tkinter é padrão no Windows)
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception:
        return None, None
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecione o arquivo CSV de entrada", filetypes=[("CSV files","*.csv"),("All files","*.*")])
    if not file_path:
        messagebox.showinfo("Cancelado", "Nenhum arquivo selecionado.")
        return None, None
    out_dir = filedialog.askdirectory(title="Selecione diretório de saída")
    if not out_dir:
        messagebox.showinfo("Cancelado", "Nenhum diretório de saída selecionado.")
        return None, None
    return file_path, out_dir

def main():
    parser = argparse.ArgumentParser(description="Processa e valida CSV de usuários.")
    parser.add_argument("input", nargs="?", help="Caminho para o arquivo CSV de entrada")
    parser.add_argument("--out", "-o", default=None, help="Diretório de saída (padrão: out)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    req_path = base_dir / "requirements.txt"
    # instalar dependências se necessário
    if req_path.exists():
        ensure_dependencies(req_path)

    # importar processor (após possível instalação)
    try:
        from processor import process_file
    except Exception:
        # forçar reload caso de ambiente alterado
        import importlib
        import processor as _p
        importlib.reload(_p)
        from processor import process_file

    input_path = args.input
    out_dir = args.out

    if not input_path:
        # modo "clicar para rodar": abrir diálogos
        input_path, out_dir = choose_paths_via_gui()
        if not input_path:
            return

    if not out_dir:
        out_dir = "out"

    try:
        result = process_file(input_path, out_dir)
    except Exception as e:
        # tentar mostrar erro via GUI se possível, senão print
        try:
            import tkinter as tk
            from tkinter import messagebox
            tk.Tk().withdraw()
            messagebox.showerror("Erro", str(e))
        except Exception:
            print("Erro:", e)
        return

    # exibir sucesso via GUI se disponível
    try:
        import tkinter as tk
        from tkinter import messagebox
        tk.Tk().withdraw()
        messagebox.showinfo("Concluído", f"Processo concluído.\nValid CSV: {result['valid_path']}\nRelatório: {result['report_path']}")
    except Exception:
        print("Concluído. Saídas:", result["valid_path"], result["report_path"])

if __name__ == "__main__":
    main()
