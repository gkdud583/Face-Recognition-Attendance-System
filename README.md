# Face_Recognition_Attendance_System

## 프로젝트 계획 이유
* 수업 전 출석을 확인하는 시간에 걸리는 시간을 줄이고, 편리하게 출석하기 위함.
* 라즈베리파이와 openCV 라이브러리 이용한 얼굴인식 오픈소스 활용한 프로젝트 진행.

## 구성요소
* 라즈베리파이
* 파이카메라

## DB설계

* student table

학생 정보를 저장하기 위함.
```
mysql> desc student;
+----------------+-------------+------+-----+---------+-------+
| Field          | Type        | Null | Key | Default | Extra |
+----------------+-------------+------+-----+---------+-------+
| student_number | int         | NO   | PRI | NULL    |       |
| major          | varchar(50) | NO   |     | NULL    |       |
| grade          | int         | NO   |     | NULL    |       |
| name           | varchar(50) | NO   |     | NULL    |       |
+----------------+-------------+------+-----+---------+-------+
```

* attendance table

출석 정보를 저장하기 위함.
```
mysql> desc attendance;
+----------------+------+------+-----+---------+-------+
| Field          | Type | Null | Key | Default | Extra |
+----------------+------+------+-----+---------+-------+
| student_number | int  | NO   | MUL | NULL    |       |
| date           | date | NO   |     | NULL    |       |
| time           | time | NO   |     | NULL    |       |
+----------------+------+------+-----+---------+-------+
```

* picture table

등록된 개인 사진의 수를 저장하기 위함.
```
mysql> desc picture;
+----------------+------+------+-----+---------+-------+
| Field          | Type | Null | Key | Default | Extra |
+----------------+------+------+-----+---------+-------+
| picture_count  | int  | NO   |     | NULL    |       |
| student_number | int  | NO   | MUL | NULL    |       |
+----------------+------+------+-----+---------+-------+

```
## 동작

* 기본 화면
> 학생 관리 창 -> 학생 추가, 검색, 수정, 삭제가 가능.<br>
  출석하기 창 -> 얼굴인식으로 출석 확인.<br>
  출석 관리 창 -> 출석 정보 확인. <br>
  사진 등록 창 -> 등록된 학생의 사진을 추가 등록.

![image](https://user-images.githubusercontent.com/60775067/119302425-113d8b00-bc9f-11eb-9cbb-5b7a164a7922.png)


* 학생 관리 창 - 추가
> DB에 등록되어 있지 않은 학생의 경우 정보를 입력하고 사진 등록을 눌러 학생 등록을 할 수 있다. <br>
> 사진 등록을 누르면 30장의 사진을 촬영해서 Dataset 디렉터리에 “User.학번.사진번호”로 저장한다. <br>
> 그리고 저장된 이미지 파일들을 불러와서 recognizer.train() 함수를 통해 저장된 이미지파일의 특징을 추출하고 recognizer.write() 함수를 통해 trainer.yml 파일로 저장한다. <br>
  입력된 학생 정보는 DB의 student 테이블에 저장한다. 
  
  ![image](https://user-images.githubusercontent.com/60775067/119302834-bbb5ae00-bc9f-11eb-9463-00bb55c644cb.png)
* 학생 관리 창 - 사진 등록

![image](https://user-images.githubusercontent.com/60775067/119303202-50b8a700-bca0-11eb-9a32-28bd59948182.png)

* 학생 관리 창 - 추가 완료

![image](https://user-images.githubusercontent.com/60775067/119303641-10a5f400-bca1-11eb-9f8d-070f0a6e3592.png)

* 학생 관리 창 - 검색
> 등록된 학생 정보를 확인할 수 있다. 기본은 전체로 되어있고 개인의 학번을 입력할 경우 한 사람의 정보만 검색할 수 있게 하였다. 
> 
![image](https://user-images.githubusercontent.com/60775067/119303956-7eeab680-bca1-11eb-868d-0edf8ac7ba62.png)

* 학생 관리 창 - 수정
> 개인의 학번을 입력하고 검색하면 DB에서 정보를 가져오도록 하였다. 수정을 하고 저장하기 버튼을 누르면 변경된 정보가 DB에 반영된다. 

![image](https://user-images.githubusercontent.com/60775067/119304035-9f1a7580-bca1-11eb-83b8-7a0eeedb0a96.png)

* 학생 관리 창 - 삭제
> 학번을 입력하고 검색 버튼을 누르면 DB에서 학생 정보를 가져오고 삭제하기 버튼을 누를 경우 DB에 있는 학생 정보와 출석 정보 그리고 dataset디렉토리에 있는 사진 파일이 삭제되도록 하였다. 

![image](https://user-images.githubusercontent.com/60775067/119304072-b0638200-bca1-11eb-97c0-f95be105f42e.png)

* 출석 관리 창 - 출석 전
> 검색을 눌러도 아직 출석한 학생이 없어 아무것도 나오지 않는 상태이다.

![image](https://user-images.githubusercontent.com/60775067/119304268-fd475880-bca1-11eb-8786-75a1c6b6516c.png)

* 출석 하기 창 - 기존에 등록된 학생의 얼굴 인식
> 출석하기에서 20초 동안 얼굴을 인식하고 인식된 얼굴과 trainer.yml파일에 추출된 각 학생의 특징과 일치하는지 확인한 후에 등록된 학생일 경우 학번이 뜨도록 하고 등록되지 않은 학생일 경우 “unknown”이 뜨도록 하였다.
> 얼굴을 인식했을 때 등록된 학생의 얼굴일 경우 attendance 테이블에 날짜, 시간, 학번을 저장하고 출석 관리 창에서 확인할 수 있도록 하였다. 

![image](https://user-images.githubusercontent.com/60775067/119304551-5dd69580-bca2-11eb-9319-8cc7edeb34b8.png)
![image](https://user-images.githubusercontent.com/60775067/119304570-64fda380-bca2-11eb-80b5-17c5a92d1335.png)

* 출석 관리 창 - 출석 후

![image](https://user-images.githubusercontent.com/60775067/119304627-7cd52780-bca2-11eb-8df9-97b92ebc833a.png)

* 사진 등록 창
> 헤어스타일의 변화, 모자 또는 마스크의 착용 여부 등에 따라 얼굴인식 결과가 달라질 수 있기 때문에 사진 등록 창을 통해 추가로 사진을 등록할 수 있도록 하였다. 

![image](https://user-images.githubusercontent.com/60775067/119304770-b3ab3d80-bca2-11eb-92eb-498c31204e82.png)
![image](https://user-images.githubusercontent.com/60775067/119304865-e2291880-bca2-11eb-9b28-77908053cf22.png)

* 사진 등록 후
> 원래 촬영된 30장의 사진에서 30장이 추가 저장된 것을 확인할 수 있다.

![image](https://user-images.githubusercontent.com/60775067/119304922-f836d900-bca2-11eb-8f07-f22affa1b32e.png)


## 얼굴 인식 오픈소스
https://m.blog.naver.com/ljy9378/221442172937

https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826


