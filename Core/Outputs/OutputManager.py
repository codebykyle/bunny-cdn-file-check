from pathlib import Path


class OutputManager:
    def __init__(self):
        self.available_outputs = []

    def register_output(self, output):
        self.available_outputs.append(output)

    def get_output_obj(self, for_file):
        for available_output in self.available_outputs:
            if available_output.does_match(Path(for_file).suffix):
                return available_output
        raise Exception("No supported file outputs")

    def save(self, result, out_file):
        output_obj = self.get_output_obj(out_file)
        output_obj.save(result, out_file)
