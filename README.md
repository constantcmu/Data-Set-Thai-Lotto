# Data Set สลากกินแบ่งรัฐบาล (หวยไทย) ย้อนหลัง

## ดึงข้อมูลมาจากหน้าเว็ป sanook.com พร้อมแนบ โค้ด python ที่ใช้ดึงข้อมูลมาด้วย

ดาต้าเซ็ท ใช้สำหรับเรียนรู้ ในงานด้าน Data โดย Python
ไม่ได้มีเจตนา เอาข้อมูลไปทำอย่างอื่น หากทีมงาน sanook ไม่สบายใจ รบกวนติดต่อมาขอลบได้

ข้อมูลใน CSV จะมีข้อมูลของทุกงวด ยกเว้น งวดปัจจุบัน ใน CSV จะแสดง xxx
เป็นเพราะหน้าเว็ป sanook แสดง xxx บนหน้าเว็ป และผมก็ ขี้เกียจจัดการ เลยบันทึกลงไปตรงๆ
หากเอาไปใช้งานจริง ควรลบ row แรกไป

# รองรับ pandas

ขอมูลใน csv ใช้งานได้บน pandas ทันที
สิ่งที่ต้องดูเป็นพิเศษคือ ในคอลัมที่มีหลายเลขที่ได้รางวัล เช่น รางวัลที่ 2 มี 5 รางวัล
จะถูกเก็บเป็น List ไว้

# วิธีรัน เพื่อ scapping ข้อมูล

1. รันคำสั่งนี้ใน Commandline เพื่อสร้าง venc

```shell
python -m venv venv  
```

2. ทำการ Activate venv

```shell
source ./venv/bin/activate
```

3. ติดตั้ง แพ็กเกจตาม requirements. txt

```shell
pip install -r requirements.txt
```

4. รัน python เพื่อเริ่ม scap

```shell
python start_scapping.py
```
