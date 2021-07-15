class Network
{
	static ERRORS = {
		NUMBERINPUT: new Error("The input must be a number")
	};
	constructor(canvasWidth, canvasHeight)
	{
		this._canvasSize = {
			w: canvasWidth,
			h: canvasHeight
		};
		this._NODESIZE = Math.floor(mainCanvasWidth / 25);
		this._nodes = new Set();
		this._rootNode = new NetworkNode(this.createCenteredVector(0, 0), 0, this.NODESIZE);
		this.nodes.add(this._rootNode);
		this.createRandomNodes(40, 3 * this.NODESIZE);
		this.createCloseConnections(this.NODESIZE * 5);
	}
	show()
	{
		for (let node of this.nodes)
		{
			node.show();
			node.showLinks();
		}
	}
	createCenteredVector(x, y)
	{
		if (typeof x!= "number" || typeof y!= "number")
		{
			throw Network.ERRORS.NUMBERINPUT;
		}
		return createVector(this.canvasSize.w * 0.5 + x, this.canvasSize.h * 0.5 + y);
	}
}