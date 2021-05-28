let input1 = "the numbers are: ";
let input2 = "0, 1, 2, 3, 4, 5, 6, 7, 8, 9\n";

let obj1ArR = [input1, input2];

function mergerFunction(text) {
    let result = text.join("");
    return result;
}

console.log(mergerFunction(obj1ArR));

class Car {

    static COLORS = {
        RED: "red",
        GREEN: "green",
        BLUE: "blue",
    }

    constructor (id, color) {
        this.id = id;

        this.color = color;
    }

    get id() {
        return this._id;
    }

    set id (id) {
        this._id = id;
    }

    get color() {
        return this._color;
    }

    set color (color) {
        this._color = color;
    }

    printCar() {
        return "The car " + this.id + " has a color = " + this.color;
    }
}

var car1 = new Car(001, Car.COLORS.RED);
var car2 = new Car(002, Car.COLORS.BLUE);
var car3 = new Car(003, Car.COLORS.GREEN);

var carArray = [car1, car2, car3];