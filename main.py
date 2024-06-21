import os
import re
import json
import properties
import subprocess
from PlasticData import PlasticData
from http.server import BaseHTTPRequestHandler, HTTPServer


def execute_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error executing command: {command}\n{result.stderr}")
    else:
        return result.stdout


def extract_branch_name(selector_output):
    match = re.search(r'smartbranch "([^"]+)"', selector_output)
    if match:
        return match.group(1)
    return None


def extract_branch_name_from_commit(commit_message):
    match = re.search(r'New checkin to `([^`]+)`', commit_message)
    if match:
        return match.group(1)
    return None


def sync_scm():
    print("Starting SCM Sync")
    os.chdir(properties.workingDirectory)
    execute_command("cm undo . -r")
    selector = execute_command("cm showselector")
    branch_name = extract_branch_name(selector)
    print(f"Current branch: {branch_name}")
    execute_command(f"cm switch {branch_name}")
    print(f"SCM Synced")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #print(f"Received GET request:\nPath: {self.path}\nHeaders: {self.headers}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'GET request received')
        if self.path == "/":
            sync_scm()
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_str = post_data.decode('utf-8')
        #print(f"Received POST request:\nHeaders: {self.headers}\nBody: {post_data_str}\n")

        try:
            plastic_data = PlasticData(post_data_str)

            self.send_response(200)
            self.end_headers()

            #print("Commit --->  " + plastic_data.content)
            os.chdir(properties.workingDirectory)
            selector = execute_command("cm showselector")
            branch_name = extract_branch_name(selector)
            branch_name_from_commit = extract_branch_name_from_commit(plastic_data.content)
            if branch_name == branch_name_from_commit:
                print(f"New check-in detected on {branch_name} branch. Syncing")
                sync_scm()
            else:
                print(f"New check-in detected on {branch_name} branch. Not gonna sync")

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON data')


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=properties.serverPort):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()