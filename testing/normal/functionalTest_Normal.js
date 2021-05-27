let input1 = "the numbers are: ";
let input2 = "0, 1, 2, 3, 4, 5, 6, 7, 8, 9\n";

let obj1ArR = [input1, input2];

function mergerFunction(text) {
    let result = text.join("");
    return result;
}

console.log(mergerFunction(obj1ArR));

