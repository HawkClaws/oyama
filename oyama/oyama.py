import os
import subprocess
import requests
import threading
from tqdm import tqdm
import time


class CommandRunner:
    def __init__(self, command: str, is_async=False):
        self.command = command
        self.is_async = is_async

    def run(self):
        print(f"command:={self.command}")

        def target():
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            output, error = process.communicate()
            if output:
                print("Output:", str(output.strip(), "utf-8"))
            if error:
                print("Error:", str(error.strip(), "utf-8"))
            if output:
                print(str(output.strip(), "utf-8"))
            rc = process.returncode
            if rc != 0:
                raise Exception(f"Command exited with error code {rc}")
            return rc

        if self.is_async:
            thread = threading.Thread(target=target)
            thread.start()
            return thread
        else:
            return target()


class ServerChecker:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.url = f"http://{self.address}:{self.port}"

    def _send_request(self):
        try:
            return requests.get(self.url)
        except requests.exceptions.ConnectionError:
            return None

    def check(self):
        response = self._send_request()
        return response is not None and response.status_code == 200

    def wait_for_server(self):
        while not self.check():
            print("Server is not ready yet. Retrying...")
            time.sleep(1)
        print("Server is ready.")


class FileDownloader:
    def __init__(self, url: str):
        self.url = url

    def download(self):  # フォルダ名を指定
        folder_name = "model"
        # フォルダが存在しない場合、作成する
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = self.url.split("/")[-1].split("?")[0]
        file_path = os.path.join(folder_name, filename)  # ファイルパスを作成

        if os.path.exists(file_path):  # ファイルが既に存在する場合はダウンロードしない
            print(f"{file_path} already exists. Skipping download.")
            return file_path

        response = requests.get(self.url, stream=True)

        file_size = int(response.headers.get("Content-Length", 0))
        progress = tqdm(
            response.iter_content(1024),
            f"Downloading {filename}",
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(file_path, "wb") as file:
            for data in progress.iterable:
                file.write(data)
                progress.update(len(data))

        return file_path


class FileWriter:
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content

    def write(self):
        with open(self.filename, "w") as f:
            f.write(self.content)


class OllamaCommandsRunner:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def run(self):
        print("creating model layer transferring model data...")
        CommandRunner(
            f"ollama create {self.model_name} -f {self.model_name}_Modelfile"
        ).run()
        CommandRunner(f"ollama run {self.model_name}").run()


def run(model_url: str = None, model_path: str = None, modelfile: str = "") -> str:
    try:
        CommandRunner(f"ollama --version").run()
    except:
        CommandRunner("curl -fsSL https://ollama.com/install.sh | sh").run()
        pass

    if ServerChecker("127.0.0.1", 11434).check() == True:
        print("Server is ready.")

    else:
        CommandRunner("ollama serve", is_async=True).run()
        ServerChecker("127.0.0.1", 11434).wait_for_server()

    try:
        CommandRunner(f"ollama pull {model_url}").run()
        print("Enable Model:" + model_url)
        return model_url
    except:
        pass

    
    
    if model_url is not None:
        model_name = model_url.split("/")[-1].split("?")[0].split(".")[0]
        filename = FileDownloader(model_url).download()
        model_path = f"./{filename}"
    else:
        model_name = model_path.split("/")[-1].split("?")[0].split(".")[0]
        
    modelfile = f"FROM {model_path}\n{modelfile}"
    print("Modelfile:\n" + modelfile)

    FileWriter(f"{model_name}_Modelfile", modelfile).write()

    OllamaCommandsRunner(model_name).run()
    print("Enable Model:" + model_name)
    return model_name
