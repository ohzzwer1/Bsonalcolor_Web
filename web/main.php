<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>브스널컬러</title>
    <link rel="stylesheet" href="main.css">
    <script>
        function test() {
            var name = document.getElementById('inputname').value;
            localStorage.setItem('name', name);
            location.href='index.php'
        }

    </script>
</head>
<body>
    <img src="https://ifh.cc/g/BcL5al.png" id="logo"/>
    <div class="explain-backdiv">
        <img src="https://ifh.cc/g/QsOtn8.png" id="brain"/>
        <div class="first-line"><div class="bold">브스널컬러</div>란?</div>
        <div class="explain-line">
            <span class="pink">브레인</span>과 <span class="pink">퍼스널컬러</span>의 합성어로 <br/>여러분의 뇌파를 측정하여
            <br/>가장 선호하는 색상을 검사하는 서비스입니다.
        </div>
        <div class="explain-line">측정된 색상으로 여러분만의 무드등을 연출해드리니,<br/>나만의 공간을 꾸밀 때 참고해보세요! 🕯</div>
    </div>
    <div class="how-title">브스널컬러 사용 안내</div>
    <img src="https://ifh.cc/g/OKWat7.png" id="how-use"/>
    <div class="text">여러분의 브스널컬러가 궁금하다면,</div>
    <input type="text" class="inputname" placeholder="이름을 입력해주세요" id="inputname"/><br/>
    <button type="button" onclick={test()}>검사하러 가기 →</button>
    <footer><div><div class="ohzz">오합지졸  숙명여대</div><div class="cr">Copyrightⓒ2023 오합지졸 숙명여대 All rights reserved.</div><u>만든 사람들</u></div></footer>
</body>
</html>