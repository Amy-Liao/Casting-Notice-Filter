# Casting Notice Filter
This repository utilizes regular expressions to filter casting messages that match users' qualifications based on gender and age.

Casting messages are frequently disseminated by agents via LINE groups in Taiwan. Typically, there are 10-20 messages daily within these groups. To expedite the process of finding relevant casting opportunities, this application allows users to specify their gender, age range, and a specific date to filter messages from.

## Demo
https://github.com/Amy-Liao/search_casting_notice_flaskapp/assets/72532191/45d1ea47-5de7-49b2-b432-5f73a1124d1f

## Usage
1. Export LINE group chat
2. Run the application using:
```
python app.py
```
3. Input your gender, preferred age range, and specify a date (messages will be filtered from this date onward)
4. Upload LINE chat text file (Sample file can be found in the repository: LINE_chat_sample.txt)

The application will generate a list of casting notices that match your criteria.
