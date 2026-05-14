import json
from supabase import create_client, Client

class SupabaseManager:
    def __init__(self, creds_json):
        self.accounts = {}
        self.active_account = None
        if creds_json:
            creds = json.loads(creds_json)
            for acc in creds:
                self.accounts[acc['label']] = create_client(acc['url'], acc['key'])
            self.active_account = list(self.accounts.keys())[0] if self.accounts else None

    def get_context_for_query(self, query):
        # Simple: search for similar stored training text
        # TODO: Semantic embeddings, better search
        acc = self.accounts[self.active_account]
        res = acc.table('training_data').select('*').execute()
        # Basic keyword match
        context = ""
        for row in res.data:
            if row and query.lower() in (row.get('content', '').lower()):
                context += "\n" + row.get('content')
        return context, self.active_account

    def add_training_text(self, label, text):
        acc = self.accounts[label] if label in self.accounts else self.accounts[self.active_account]
        acc.table('training_data').insert({"content": text}).execute()

    def add_account(self, creds):
        self.accounts[creds['label']] = create_client(creds['url'], creds['key'])

    def list_accounts(self):
        return list(self.accounts.keys())
