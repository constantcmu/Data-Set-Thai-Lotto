import pandas as pd
"""
สคริปต์นี้ประมวลผลไฟล์ CSV ที่มีข้อมูลรางวัลลอตเตอรี่และแก้ไขคอลัมน์ 'prize_pre_3digit' 
หากมีค่าที่ว่างเปล่า สคริปต์ทำตามขั้นตอนดังนี้:
1. โหลดไฟล์ CSV เข้าไปใน pandas DataFrame
2. วนลูปผ่านแต่ละแถวของ DataFrame
3. สำหรับแถวที่ 'prize_pre_3digit' ว่างเปล่า (เช่น "['', '']"):
    - หาก 'prize_sub_3digits' มีมากกว่า 2 องค์ประกอบ ให้กำหนด 2 องค์ประกอบแรกให้กับ 'prize_pre_3digit'
    - ลบ 2 องค์ประกอบแรกออกจาก 'prize_sub_3digits'
4. หาก 'prize_sub_3digits' มีมากกว่า 2 องค์ประกอบหลังจากขั้นตอนข้างต้น ให้ลบองค์ประกอบสุดท้ายออก
5. อัปเดต DataFrame ด้วยค่าที่แก้ไขของ 'prize_pre_3digit' และ 'prize_sub_3digits'
6. บันทึก DataFrame ที่แก้ไขแล้วลงในไฟล์ CSV ใหม่
Dependencies:
- pandas
การใช้งาน:
- ตรวจสอบให้แน่ใจว่าไฟล์ CSV อินพุต 'lotto_prize_3digit.csv' อยู่ในไดเรกทอรีเดียวกับสคริปต์นี้
- รันสคริปต์เพื่อสร้าง 'lotto_prize_3digit_fixed.csv' ที่มีข้อมูลที่ถูกต้อง
"""

# Load the CSV file
df = pd.read_csv('lotto_prize_3digit.csv')

# Iterate through the rows and fix the empty prize_pre_3digit
for index, row in df.iterrows():
    prize_sub_3digits = eval(row['prize_sub_3digits'])
    if row['prize_pre_3digit'] == "['', '']":
        if len(prize_sub_3digits) > 2:
            df.at[index, 'prize_pre_3digit'] = str(prize_sub_3digits[:2])
            prize_sub_3digits = prize_sub_3digits[2:]
    if len(prize_sub_3digits) > 2:
        prize_sub_3digits = prize_sub_3digits[:-1]
    df.at[index, 'prize_sub_3digits'] = str(prize_sub_3digits)

# Save the fixed CSV file
df.to_csv('lotto_prize_3digit_fixed.csv', index=False)
