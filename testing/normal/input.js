class Network {
    static ERRORS = {
        NUMBERINPUT: new Error("The input must be a number")
    };

    constructor(canvasWidth, canvasHeight) {
        this._canvasSize = {w: canvasWidth, h:canvasHeight};
        this._NODESIZE = Math.floor(mainCanvasWidth / 25);

        this._nodes = new Set();
        
        this._rootNode = new NetworkNode(
            this.createCenteredVector(0, 0),
            0, 
            this.NODESIZE
        );


        this.nodes.add(this._rootNode);
        this.createRandomNodes(40, 3 * this.NODESIZE);
        this.createCloseConnections(this.NODESIZE * 5);

    }

    show() {
        for (let node of this.nodes) {
            node.show();
            node.showLinks();
        }
    }

    // GETTERS AND SETTERS
    /**
     * Size of the current canvas where the nodes are placed.
     * @returns {w: XXXXX, h:YYYYY} object with the width (XXXXX) and the height (YYYYY) of the canvas in pixels.
     */
    get canvasSize() {
        return this._canvasSize;
    }
    
    /**
     * @returns the intended size of the nodes as a number.
     */
    get NODESIZE() {
        return this._NODESIZE;
    }

    /**
     * @returns the set of NetworkNodes stored on the object.
     */
    get nodes() {
        return this._nodes;
    }

    // ELEMENTS CREATION
    // NODE
    createRandomNodes(N, R) {
        let MAXATTEMPS = 1000;
        let attempt, pos, node, validNode;
        let index = 1;
        for (let i = 0; i < N; i++) {
            validNode = false;
            attempt = 0;
            while (!validNode && attempt++ < MAXATTEMPS) {
                validNode = true;
                pos = createVector(
                    Math.floor(Math.random() * (this.canvasSize.w - this.NODESIZE * 2)) + this.NODESIZE,
                    Math.floor(Math.random() * (this.canvasSize.h - this.NODESIZE * 2)) + this.NODESIZE
                );
                node = new NetworkNode(pos, index, this.NODESIZE);
                for (let otherNode of this.nodes) {
                    if (node.dist(otherNode) <= R) {
                        validNode = false;
                        break;
                    }
                }
            }
            if (validNode) {
                this.nodes.add(node);
                index++;
            }
        }
    }
    // LINK
    createCloseConnections(maxDistance) {
        for (let node of this.nodes) {
            for (let mateNode of this.nodes) {
                if (mateNode == node) {
                    continue
                }
                if (node.dist(mateNode) <= maxDistance) {
                    node.addConnection(mateNode)
                }
            }
        }
    }

    // NODE MANIPULATION
    

    // TOOLS
    /**
     * Creates a p5.Vector with the position given from the center of the screen.
     * @param {int} x horizontal position from center
     * @param {int} y vertical position from center
     * @returns p5.Vector with the desired coordinates
     */
    createCenteredVector(x, y) {
        if (typeof x != "number" || typeof y != "number") {
            throw Network.ERRORS.NUMBERINPUT;
        }
        return createVector(
            this.canvasSize.w * 0.5 + x,
            this.canvasSize.h * 0.5 + y
        );
    }
}