from audio import Audio
# CustomChart class, inherits from audio
# Allows player to make custom levels


class CustomChart(Audio):
    def __init__(self, chart_file_path: str, file_path: str=None):
        super().__init__(file_path)
        self.chart_file_path = chart_file_path
        self.file_path = file_path

    def read_chart(self):
        # Opens text file, writes notes to array and formats so game can read it
        chart_file = open(self.chart_file_path, "r")
        self.notes_to_spawn = chart_file.readlines()
        self.notes_array = []
        for i in range(len(self.notes_to_spawn)):
            self.notes_array.append(self.notes_to_spawn[i].split(" "))
        print(self.notes_array)
        for i in range(len(self.notes_array)):
            self.notes_array[i][1] = self.notes_array[i][1].replace("\n", "")

        print(self.notes_array)
        chart_file.close()
        return self.notes_to_spawn