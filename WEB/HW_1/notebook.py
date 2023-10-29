import pickle


class Note:
    def __init__(self, name):
        self.text = ''
        self.name = name
        self.tags = []

    def __le__(self, other):
        return self.name <= other.name

    def __repr__(self):
        return f"Note: {self.name} Contents: {self.text}"

    def edit_text(self, text):
        self.text = text

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)


class Notebook:
    def __init__(self):
        self.notes = []
        self.tag_dictionary = {}
        self.load_data()

    def add_tags(self, note, tags):
        for tag in tags:
            if tag in self.tag_dictionary:
                self.tag_dictionary[tag].append(note)
                note.add_tag(tag)
            else:
                self.tag_dictionary[tag] = [note]
                note.add_tag(tag)

    def remove_tag(self, tag):
        notes = self.search_notes_by_tag(tag)
        for note in notes:
            note.remove_tag(tag)
        self.tag_dictionary.pop(tag, None)

    def add_note(self, note):
        self.notes.append(note)

    def edit_note(self, note_name, new_text):
        notes_to_edit = self.search_notes_by_name(note_name)
        for note in notes_to_edit:
            note.edit_text(new_text)

    def delete_note(self, note_name):
        notes_to_delete = self.search_notes_by_name(note_name)
        for note in notes_to_delete:
            self.notes.remove(note)

        for tag in self.tag_dictionary:
            results = self.tag_dictionary[tag]
            for nt in results:
                if nt.name == note_name:
                    self.tag_dictionary[tag].remove(nt)

    def view_notes(self):
        for note in self.notes:
            print(f"Title: {note.name}")
            print(f"Text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
        print(f"Tags: {','.join(self.tag_dictionary.keys())}")

    def get_sorted_note_names(self):
        sorted_names = sorted([note.name for note in self.notes])
        return sorted_names

    def search_notes_by_name(self, note_name):
        return [note for note in self.notes if note.name == note_name]

    def search_notes_by_tag(self, tag):
        return self.tag_dictionary.get(tag, [])

    def search_notes_by_text(self, query):
        return [note for note in self.notes if query in note.text]

    def load_data(self):
        try:
            with open('notebook.pkl', 'rb') as file:
                loaded_notebook = pickle.load(file)
                self.notes = loaded_notebook.notes
                self.tag_dictionary = loaded_notebook.tag_dictionary
        except FileNotFoundError:
            self.notes = []
            self.tag_dictionary = {}

    def save_data(self):
        with open('notebook.pkl', 'wb') as file:
            pickle.dump(self, file)