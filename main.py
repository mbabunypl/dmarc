from backend.unzipper import unzip_reports
import parsedmarc



unzip_reports('reports')







def parse_dmarc_and_write_to_json(xml_file_path, json_file_path):
    # Parse DMARC report using parsedmarc
    dmarc_report = parsedmarc.parse_report_file(xml_file_path)

    # Write the DMARC report to a JSON file with indentation
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(dmarc_report, json_file, ensure_ascii=False, indent=4)

# Example usage
xml_file_path = 'test.xml'
json_file_path = 'dmarc_report.json'


parse_dmarc_and_write_to_json(xml_file_path, json_file_path)

