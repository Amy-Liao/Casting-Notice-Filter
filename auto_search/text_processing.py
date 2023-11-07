import os
import re
import typing

def extract_messages_from_file(search_file, search_date:str, age_lower:int, age_upper:int, gender:typing.Literal['F', 'M'])->[{}]:
    messages = []  # Create a list to store extracted messages
    cnt = 1
    search_date = search_date.replace('-', '/')
    date_msg_pattern = r"\d{4}\/\d{2}\/\d{2}, (Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
    search_file.seek(0, os.SEEK_END)
    file_size = search_file.tell()
    buffer = bytearray()  # Create a byte buffer

    for pos in range(file_size - 1, -1, -1):
        search_file.seek(pos)
        char = search_file.read(1)

        if char == b'\r':
            message = buffer[::-1].decode().strip()
            message = message.replace('\n', '<br>')
            print(message)
            if message.startswith(search_date):
                messages.append({'title': cnt, 'content': "⬆️ Since "+message})
                break
            elif re.match(date_msg_pattern, message):
                messages.append({'title': cnt, 'content': "⬆️ Since "+message})
                cnt += 1
            elif message!="":
                qualified, fit_age, fit_gen = extract_message(message, age_lower, age_upper, gender)
                if qualified:
                    messages.append({'title': cnt, 'fit_age': fit_age, 'fit_gen': fit_gen, 'content': message})
                    cnt += 1
            buffer = bytearray()
        else:
            buffer.extend(char)
    return messages

def extract_message(message:str, my_age_lower:int, my_age_upper:int, my_gender:typing.Literal['F', 'M']) -> bool:
    """
    Parameters
        message: str, the message we want to check
        my_age_lower: int, the lower bound of age we want to check in message
        my_age_upper: int, the upper bound of age we want to check in message
        my_gender: 'F' or 'M', the gender we want to check in message. 
    Return
        bool
    """
    age_qualified = 0
    gender_qualified = 0
    fit_age = []
    fit_gen = []

    def check_range(require_range, my_age_upper, my_age_lower):
        """
        Check if my age range overlaps with the require range
        Returns: 
            bool (True if the range overlaps; otherwise, False)
        """
        if my_age_lower<=require_range[1] and require_range[1]<=my_age_upper:
            return True
        elif require_range[0]<=my_age_upper and my_age_upper<=require_range[1]:
            return True
        return False
    # Extract character age, character gender, and filming dates using regex
    character_age_pattern = r"[\(（]\d{2}[-~～]\d{2}[\)）]|\d{2}[-~～]\d{2}\s*[yY歲]|\d{2,3}\s*[yY歲]"
    character_gender_pattern = r"(男|女|male|female)"
    character_ages = re.findall(character_age_pattern, message)
    character_genders = re.findall(character_gender_pattern, message)
    print(f"Character ages: {character_ages}")
    
    # Check "Age" data
    if len(character_ages)==0:
        age_qualified = -1          # message didn't mention age
    else:
        number_only_pattern = r"(\d+[-~～]?\d+)"
        for ch_age in character_ages:
            age = re.search(number_only_pattern, ch_age).group()
            if age.isdigit():           # case that the messsage specified age
                if (my_age_lower<=int(age)) and (int(age)<=my_age_upper):
                    print(ch_age)
                    fit_age.append(ch_age)
                    age_qualified = 1
            else:                       # case that the message contains age range  
                for delimiter in ['-', '~', '～']:
                    if (delimiter in age):
                        require_age = list(map(int, age.split(delimiter)))
                        if check_range(require_age, my_age_upper, my_age_lower):
                            age_qualified = 1
                            print(ch_age)
                            fit_age.append(ch_age)
                            break

    # Check "Gender" data
    if len(character_genders)==0:
        gender_qualified = -1        # message didn't mention gender
    else:
        for gender in character_genders:
            if my_gender=='F' and (gender=="female" or gender=="女"):
                print(gender)
                fit_gen.append(gender)
                gender_qualified = 1
            elif my_gender=='M' and (gender=="male" or gender=="男"):
                print(gender)
                fit_gen.append(gender)
                gender_qualified = 1

    if age_qualified==1 and gender_qualified==1:
        return True, fit_age, fit_gen
    elif age_qualified==1 and gender_qualified==-1:
        return True, fit_age, fit_gen
    elif age_qualified==-1 and gender_qualified==1:
        return True, fit_age, fit_gen
    else:
        return False, fit_age, fit_gen