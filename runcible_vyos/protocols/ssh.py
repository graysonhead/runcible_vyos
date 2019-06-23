from runcible.protocols.protocol import TerminalProtocolBase
from runcible.core.errors import RuncibleValidationError, RuncibleNotConnectedError
from time import sleep
import paramiko
import re


ansi_regex = r'\x1b(' \
             r'(\[\??\d+[hl])|' \
             r'([=<>a-kzNM78])|' \
             r'([\(\)][a-b0-2])|' \
             r'(\[\d{0,2}[ma-dgkjqi])|' \
             r'(\[\d+;\d+[hfy]?)|' \
             r'(\[;?[hf])|' \
             r'(#[3-68])|' \
             r'([01356]n)|' \
             r'(O[mlnp-z]?)|' \
             r'(/Z)|' \
             r'(\d+)|' \
             r'(\[\?\d;\d0c)|' \
             r'(\d;\dR))'

ansi_purge = re.compile(ansi_regex, flags=re.IGNORECASE)

class VyosInteractiveSSH(TerminalProtocolBase):

    def __init__(self, config: dict):
        super().__init__(config=config)
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.prompt = None

    def validate(self, config):
        for key in ['hostname', 'username']:
            if key not in config:
                raise RuncibleValidationError(msg=f"Key {key} missing from Protocol {self.__repr__()}")

    def connect(self):
        self.client.connect(hostname=getattr(self, 'hostname', None),
                            username=getattr(self, 'username', None),
                            password=getattr(self, 'password', None),
                            timeout=getattr(self, 'timeout', 5))
        self.terminal = self.client.invoke_shell()
        self.terminal.settimeout(getattr(self, 'timeout', 5))
        sleep(.5)
        lines = self.read_lines(65535)
        self.prompt = lines[-1].strip(':~$#')
        return lines

    def read_until_prompt(self):
        return self.read_until_pattern(f'{self.prompt}.*')

    def send_implement(self, command):
        if not getattr(self, 'terminal', None):
            raise RuncibleNotConnectedError
        self.terminal.send(command + '\n')
        return self.read_until_prompt()

    def read_lines(self, num_bytes=65535):
        raw_output = self.terminal.recv(num_bytes)
        output_lines = raw_output.decode().split('\n')
        clean_lines = []
        for line in output_lines:
            new_line = line.strip('\n').strip('\r').strip()
            clean_lines.append(new_line)
        return clean_lines

    def read(self, num_bytes=65535):
        line = self.terminal.recv(num_bytes).decode()
        # Vyos returns a ton of ANSI escape sequences that are meaningless to us
        line = ansi_purge.sub('', line)
        return line

    def read_until_pattern(self, pattern):
        sleep(.5)
        while True:
            string = self.read()
            lines = string.splitlines()
            if lines.__len__() > 1:
                if re.match(pattern, lines[-1]):
                    break
        return lines