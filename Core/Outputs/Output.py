from Core.Results.LibraryResult import LibraryResult

class Output:
    def does_match(self,  input):
        return True

    def save(self, library_result: LibraryResult, outfile: str):
        raise Exception("No save format specified for outfile")

    def __str__(self):
        return 'Unknown File Type'