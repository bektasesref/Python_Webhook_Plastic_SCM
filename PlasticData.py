import json

class PlasticData:
    def __init__(self, raw_data):
        data_dict = json.loads(raw_data)
        self.user = data_dict.get('PLASTIC_USER'),
        self.client_machine = data_dict.get('PLASTIC_CLIENTMACHINE'),
        self.server = data_dict.get('PLASTIC_SERVER'),
        self.comment = data_dict.get('PLASTIC_COMMENT'),
        self.changeset = data_dict.get('PLASTIC_CHANGESET'),
        self.merge_links = data_dict.get('PLASTIC_MERGE_LINKS'),
        self.shelve = data_dict.get('PLASTIC_SHELVE'),
        self.input_data = data_dict.get('INPUT'),
        self.content = data_dict.get('content')

    def __repr__(self):
        return (f"PlasticData(user={self.user}, client_machine={self.client_machine}, server={self.server}, "
                f"comment={self.comment}, changeset={self.changeset}, merge_links={self.merge_links}, "
                f"shelve={self.shelve}, input_data={self.input_data}, content={self.content})")