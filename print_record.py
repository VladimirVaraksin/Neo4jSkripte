def print_records(title, records):
    print(f"=== {title} ===")
    record_list = list(records)
    if not record_list:
        print("No records found.")
        return
    headers = list(record_list[0].data().keys())
    col_width = 20
    header_row = "".join(f"{header:<{col_width}}" for header in headers)
    separator = "-" * (col_width * len(headers))
    print(header_row)
    print(separator)
    for record in record_list:
        row_values = [str(val) for val in record.data().values()]
        print("".join(f"{val:<{col_width}}" for val in row_values))
    print("")
