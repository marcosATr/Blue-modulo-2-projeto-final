const ingrsParent = document.querySelector('.ingredients')
ingrsList = ingrsParent.innerHTML.split(', ')
console.log(ingrsList)
let newUl = document.createElement('ul')
ingrsParent.innerHTML = ''
for (i of ingrsList){
  let newLi = document.createElement('li')
  newLi.innerHTML = i.toLowerCase()
  newUl.append(newLi)
  //console.log(newUl)
  ingrsParent.append(newUl)
}
