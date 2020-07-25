const mainBoxRow1 = document.querySelectorAll(".main-box__category");

// function handleClick() {
//     category.classList.toggle(CLICKED_CLASS);
// }


//// main_box__category 중 클릭된 항목의 CSS를 변경하는 기능
// main_box__category의 요소들을 불러와서 클릭되면 함수를 실행한다.
mainBoxRow1.forEach(item => {
    item.addEventListener("click", convertRed);
})

// 클릭한 태그를 빨간색으로 바꿈.
function convertRed(event) {
    event.preventDefault(); // 클릭한 후 마우스를 떼어도 기능이 유지되로록 설정.
    targetClassList = event.currentTarget.classList; // 클릭된 요소의 클래스 리스트를 불러옴.
    targetClassList.add('clicked_category');

    categoryNum = targetClassList[1]; // targetClass의 main-box__category(n)을 가져옴
    remainClassList = removeTargetClass(categoryNum); // 선택되지 않은 요소들을 배열로 만듦.
    remainClassList.forEach(item => console.log(mainBoxRow1.querySelector(item)));
    // console.log(remainClassList);
    

    // testClass = allClassList.filter(targetClassList[1]);
    // console.log(testClass);
}

// 클릭되지 않은 요소의 클래스를 불러옴.
function removeTargetClass(categoryNum) {
    allClassList = ['main-box__category1', 'main-box__category2', 'main-box__category3'];
    allClassList.splice(allClassList.indexOf(categoryNum), 1);
    return allClassList
}

// function myTest(nonSelectedClass) {
//     my_test = mainBoxRow1.querySelector(nonSelectedClass);
//     console.log(my_test);
// }

// // mina_box__category의 각 요소들을 불러옴.
// mainBoxRow1.forEach(function(element) {
//     loadClassList(element);
// });

// // 개별 태그들의 클래스 리스트를 출력
// function loadClassList(eachElement){
//     console.log(eachElement.classList);
// }


