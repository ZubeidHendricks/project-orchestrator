import os
import json
from datetime import datetime
from github import Github
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self, token):
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo('ZubeidHendricks/project-orchestrator')
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def generate_audit_log(self):
        """Create comprehensive audit log"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'events': []
        }
        
        # Log repository events
        for event in self.project_repo.get_events():
            encrypted_event = self.cipher_suite.encrypt(
                json.dumps({
                    'type': event.type,
                    'actor': event.actor.login,
                    'created_at': event.created_at.isoformat()
                }).encode()
            )
            
            audit_log['events'].append({
                'encrypted_event': encrypted_event.decode()
            })
        
        # Save encrypted log
        os.makedirs('logs', exist_ok=True)
        with open('logs/audit_log.json', 'w') as f:
            json.dump(audit_log, f, indent=2)
    
    def decrypt_audit_log(self):
        """Decrypt and verify audit log"""
        with open('logs/audit_log.json', 'r') as f:
            encrypted_log = json.load(f)
        
        decrypted_events = []
        for event in encrypted_log['events']:
            decrypted_event = self.cipher_suite.decrypt(
                event['encrypted_event'].encode()
            )
            decrypted_events.append(json.loads(decrypted_event))
        
        return decrypted_events

def main():
    token = os.environ.get('GHUB_TOKEN')
    security_manager = SecurityManager(token)
    security_manager.generate_audit_log()

if __name__ == '__main__':
    main()