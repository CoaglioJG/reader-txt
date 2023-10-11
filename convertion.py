import struct
import os

def convertion():
    print("Script de conversão iniciado")
    forExecute = input("Enter the directory where the files to be converted are located: ")
    forSave = input("Enter the directory where the conversions will be saved: ")

    for root, _, files in os.walk(forExecute):
        for file in files:
            file_path1 = os.path.join(root, file)
            parts = file_path1.split('\\')
            last_part = parts[-1]
            file_name, type_file = os.path.splitext(last_part)
            data_format = "I 9s I 58s f f f f f f f f f f f"   # Formato: int, string de 32 bytes, int, string de 32 bytes, floats
            data_format_header = "32s 32s 32s 32s 32s 32s 32s 32s 32s 32s 32s 32s 32s 32s 32s"
            data_size = struct.calcsize(data_format)
            count = 0

            encodings = ['utf-8', 'utf-16', 'latin-1','cp1252']
                
            if(type_file == '.dat'):
                    with open(file_path1, "rb") as input_file, open(forSave+'\\'+file_name+'.csv', "w") as output_file:
                        while True:   
                            if count <= 3:
                                header_data = struct.unpack(data_format_header, input_file.read(struct.calcsize(data_format_header)))
                                # print(count, header_data)

                                creature_header0, creature_header1, creature_header2, creature_header3, creature_header4, creature_header5, creature_header6, creature_header7, creature_header8, creature_header9, creature_header10, creature_header11, creature_header12, creature_header13, creature_header14 = header_data

                                decoded_headers = []
                                for header in header_data:
                                    for encoding in encodings:
                                        try:
                                            decoded_header = header.decode(encoding).strip()
                                            decoded_headers.append(decoded_header)
                                            break
                                        except UnicodeDecodeError:
                                            continue
                                formatted_line = ",".join(decoded_headers) + "\n"

                                output_file.write(formatted_line)
                            if count > 3:
                                packed_data = input_file.read(data_size)

                                if not packed_data:
                                    break

                                # Desempacotar os dados
                                unpacked_data = struct.unpack(data_format, packed_data)
                                # print(unpacked_data)
                                style, action, index, animation, start_inter, end_inter, time_length, swing, strike, timing, split, timing2, freeze, effect, cancelTime = unpacked_data

                                # Converter campos para texto e remover espaços vazios
                                action_text = action.decode("utf-8").strip()
                                # print(animation)
                                animation_text = animation.decode("utf-8").strip()
                                start_inter_formatted= round(start_inter,2)
                                end_inter_formatted = round(end_inter,2)
                                time_length_formatted = round(time_length, 2)
                                swing_formatted = round(swing, 2)
                                strike_formatted = round(strike, 2)
                                timing_formatted = round(timing, 2)
                                split_formatted = round(split, 2)
                                timing2_formatted = round(timing2, 2)
                                freeze_formatted = round(freeze, 2)
                                effect_formatted = round(effect, 2)
                                cancelTime_formatted = round(cancelTime, 2)

                                action_text_aligned = action_text.ljust(20)

                                # Criar uma string formatada com espaços ajustados
                                formatted_line = f"{style},{action_text},{index},{animation_text},{start_inter_formatted},{end_inter_formatted},{time_length_formatted},{swing_formatted},{strike_formatted},{timing_formatted},{split_formatted},{timing2_formatted},{freeze_formatted},{effect_formatted},{cancelTime_formatted}\n"

                                # Escrever a string formatada no arquivo de saída
                                output_file.write(formatted_line)

                            count += 1

                    print("Convertion of binary for text finish.")

            if(type_file == '.csv'):
                # Abrir arquivos de entrada e saída
                    with open(file_path1, "r") as input_file, open(forSave+'\\'+file_name+'.dat', "wb") as output_file:
                        lines = input_file.readlines()

                        creature_data = struct.pack(data_format_header,lines[0].split(',')[0].encode("utf-8"), lines[0].split(',')[1].encode("utf-8"), b"", b"", b"", b"", b"", b"", b"",b"", b"", b"", b"", b"",b"")
                        index_data = struct.pack(data_format_header,lines[1].split(',')[0].encode("utf-8"), lines[1].split(',')[1].encode("utf-8"), b"", b"", b"", b"", b"", b"", b"",b"", b"", b"", b"", b"",b"")
                        skeleton_data = struct.pack(data_format_header,lines[2].split(',')[0].encode("utf-8"),lines[2].split(',')[1].encode("utf-8"), b"", b"", b"", b"", b"", b"", b"",b"", b"", b"", b"", b"",b"")
                        empty_data = struct.pack(data_format_header,b"",b"", b"", b"", b"", b"", b"", b"", b"",b"", b"", b"", b"", b"",b"")


                        output_file.write(creature_data)
                        output_file.write(index_data)
                        output_file.write(skeleton_data)
                        output_file.write(empty_data)
                        
                        for idx, line in enumerate(lines):
                            line = line.strip() # Remover espaços em branco no início e no fim
                            fields = line.split(',')

                            if(idx <= 4):
                                continue

                            for field in fields:
                                    if(field ==''):
                                        continue

                                # Extrair os campos relevantes
                                    style = int(fields[0])
                                    action = fields[1].encode("utf-8")
                                    index = int(fields[2])
                                    animation = fields[3].encode("utf-8")
                                    start_inter = float(fields[4])
                                    end_inter = float(fields[5])
                                    time_length = float(fields[6])
                                    swing = float(fields[7])
                                    strike = float(fields[8])
                                    timing = float(fields[9])
                                    split = float(fields[10])
                                    timing2 = float(fields[11])
                                    freeze = float(fields[12])
                                    effect_text = fields[13].strip()
                                    cancelTime = float(fields[14])

                                    if effect_text:
                                        try:
                                            effect = float(effect_text)
                                        except ValueError:
                                            effect = 0  # A conversão falhou, atribua 0.0
                                    else:
                                        effect = 0

                                # Empacotar e escrever no arquivo binário
                            packed_data = struct.pack(data_format, style, action, index, animation, start_inter, end_inter,
                                                        time_length, swing, strike, timing, split, timing2, freeze,effect,cancelTime)
                            
                            output_file.write(packed_data)

                    print("Convertion success.")


convertion()