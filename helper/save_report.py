from amagi_library.helper.workdir import WorkDirectory

import os
import uuid

class SaveReport(object):

    def __init__(self, headers=None, fields=None):
        self.headers = headers
        self.fields = fields

    def save_report(self, obj_list, format, file_path = None):
        methods = {
            "csv" : self.save_report_as_csv
        }
        if format not in methods:
            raise Exception("{} format is not supported".format(format))
        return methods[format](obj_list, format, file_path)

    def get_fields(self, obj_list):
        keys = None
        if obj_list and len(obj_list) > 0:
            keys = obj_list[0].keys()
        return keys

    def save_report_as_csv(self, obj_list, format, file_path=None):
        if not file_path:
            work_dir = WorkDirectory(prefix="save_report").get_work_dir()
            file_path = os.path.join(work_dir, f"{uuid.uuid1()}.{format}")
        
        with open(file_path, 'w') as file:
            header_text = None
            header_list = self.headers if self.headers else self.get_fields(obj_list)
            row_text = ",".join(header_list) if header_list else None
            if header_text:
                file.write(row_text)
                file.write("\n")

            if not self.fields:
                self.fields = header_list

            for item in obj_list:
                row = []
                for field in self.fields:
                    if field in item:
                        row.append(item[field])
                    else:
                        row.append("NA")
                converted_row = map(lambda cell : f"\"{cell}\"", row)
                row_text = ",".join(converted_row)
                file.write(row_text)
                file.write("\n")

        return file_path