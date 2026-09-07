from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HOST = "127.0.0.1"
PORT = 8000


HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cronômetro</title>
    <style>
        :root {
            color-scheme: light;
            --ink: #172033;
            --muted: #68748a;
            --paper: #f6f8fb;
            --panel: rgba(255, 255, 255, 0.88);
            --line: #dce3ed;
            --green: #16805b;
            --amber: #b86c00;
            --red: #c33f4b;
        }

        * { box-sizing: border-box; }

        body {
            min-height: 100vh;
            margin: 0;
            display: grid;
            place-items: center;
            padding: 24px;
            color: var(--ink);
            font-family: Georgia, "Times New Roman", serif;
            background:
                radial-gradient(circle at 12% 10%, #dcece6 0, transparent 34%),
                radial-gradient(circle at 90% 90%, #f4e4ce 0, transparent 32%),
                var(--paper);
        }

        main {
            width: min(100%, 620px);
            padding: clamp(28px, 7vw, 64px);
            text-align: center;
            background: var(--panel);
            border: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: 0 24px 70px rgba(35, 52, 76, 0.13);
            backdrop-filter: blur(12px);
            animation: arrive 500ms ease-out both;
        }

        .eyebrow {
            margin: 0 0 10px;
            color: var(--green);
            font: 700 0.75rem/1.2 Arial, sans-serif;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        h1 {
            margin: 0 0 30px;
            font-size: clamp(2rem, 7vw, 3.4rem);
            font-weight: 500;
            letter-spacing: 0;
        }

        .visor {
            margin: 0 0 32px;
            padding: 24px 12px;
            color: #10233a;
            background: #fff;
            border: 1px solid var(--line);
            font: 700 clamp(2.7rem, 11vw, 5rem)/1 "Courier New", monospace;
            letter-spacing: 0;
            box-shadow: inset 0 0 0 5px #f7f9fc;
        }

        .status {
            min-height: 1.4em;
            margin: -18px 0 22px;
            color: var(--muted);
            font: 0.9rem Arial, sans-serif;
        }

        .botoes {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        button {
            min-width: 120px;
            padding: 14px 18px;
            border: 0;
            color: white;
            font: 700 0.95rem Arial, sans-serif;
            cursor: pointer;
            transition: transform 150ms ease, filter 150ms ease;
        }

        button:hover { filter: brightness(1.08); transform: translateY(-2px); }
        button:active { transform: translateY(0); }
        button:focus-visible { outline: 3px solid #1f2937; outline-offset: 3px; }
        .iniciar { background: var(--green); }
        .pausar { background: var(--amber); }
        .resetar { background: var(--red); }

        .atalho {
            margin: 28px 0 0;
            color: var(--muted);
            font: 0.78rem Arial, sans-serif;
        }

        kbd {
            padding: 3px 7px;
            border: 1px solid var(--line);
            background: #fff;
            font-family: Arial, sans-serif;
        }

        @keyframes arrive {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 520px) {
            .botoes { flex-direction: column; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
    <main>
        <p class="eyebrow">Controle de tempo</p>
        <h1>Cronômetro</h1>
        <div id="visor" class="visor" role="timer" aria-live="polite">00:00:00</div>
        <p id="status" class="status">Pronto para começar</p>
        <div class="botoes">
            <button class="iniciar" type="button" id="iniciar">Iniciar</button>
            <button class="pausar" type="button" id="pausar">Pausar</button>
            <button class="resetar" type="button" id="resetar">Resetar</button>
        </div>
        <p class="atalho">Atalho: <kbd>Espaço</kbd> inicia ou pausa</p>
    </main>
    <script>
        const visor = document.querySelector("#visor");
        const status = document.querySelector("#status");
        let totalMs = 0;
        let inicio = 0;
        let rodando = false;
        let frameId;

        function formatar(ms) {
            const totalSegundos = Math.floor(ms / 1000);
            const horas = Math.floor(totalSegundos / 3600);
            const minutos = Math.floor((totalSegundos % 3600) / 60);
            const segundos = totalSegundos % 60;
            return [horas, minutos, segundos]
                .map(valor => String(valor).padStart(2, "0"))
                .join(":");
        }

        function atualizar() {
            const atual = rodando ? totalMs + (performance.now() - inicio) : totalMs;
            visor.textContent = formatar(atual);
            if (rodando) frameId = requestAnimationFrame(atualizar);
        }

        function iniciar() {
            if (rodando) return;
            rodando = true;
            inicio = performance.now();
            status.textContent = "Em execução";
            atualizar();
        }

        function pausar() {
            if (!rodando) return;
            totalMs += performance.now() - inicio;
            rodando = false;
            cancelAnimationFrame(frameId);
            status.textContent = "Pausado";
            atualizar();
        }

        function resetar() {
            rodando = false;
            cancelAnimationFrame(frameId);
            totalMs = 0;
            status.textContent = "Pronto para começar";
            atualizar();
        }

        document.querySelector("#iniciar").addEventListener("click", iniciar);
        document.querySelector("#pausar").addEventListener("click", pausar);
        document.querySelector("#resetar").addEventListener("click", resetar);
        document.addEventListener("keydown", event => {
            if (event.code !== "Space" || event.target.matches("button")) return;
            event.preventDefault();
            rodando ? pausar() : iniciar();
        });
    </script>
</body>
</html>"""


class CronometroWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return

        conteudo = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

    def log_message(self, formato, *args):
        return


if __name__ == "__main__":
    servidor = ThreadingHTTPServer((HOST, PORT), CronometroWebHandler)
    print(f"Cronômetro web disponível em http://{HOST}:{PORT}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()