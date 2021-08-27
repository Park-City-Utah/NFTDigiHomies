pragma solidity 0.6.6;

import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract DigiHomie is ERC721, VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;
    uint256 public rando;
    enum Body {
        ThinLight,
        ThinMid,
        ThinDark,
        ThickLight,
        ThickMid,
        ThickDark
    }

    //mapping(uint256 => string) Body;

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Body) public tokenIdToBody;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectable(bytes32 indexed requestId);

    constructor(
        address _VRFCoordinator,
        address _LinkToken,
        bytes32 _keyhash
    )
        public
        VRFConsumerBase(_VRFCoordinator, _LinkToken)
        ERC721("DigiHomies", "DH")
    {
        keyHash = _keyhash;
        fee = 0.1 * 10**18; //.1 LINK 1000000000000000000
        tokenCounter = 0;
    }

    //Creates contract for each homie
    function createHomie(string memory tokenURI) public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        //chainlink returns request and random, need to map
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectable(requestId); //logging & testing
    }

    //Return randomness
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        address homieOwner = requestIdToSender[requestId]; //return from mapping owner
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter; //Start at 0.. 1? edit above
        _safeMint(homieOwner, newItemId);
        _setTokenURI(newItemId, tokenURI); //Optional
        //write randomnumber to py??
        Body body = Body(randomness % 6); //1-4
        tokenIdToBody[newItemId] = body;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
        // rando = randomNumer;        //Saves to global value, might be able to send to pythong
    }

    //Set metadata
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner or approved."
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    //Returns random number
    /*function getRandomNumber() public returns (bytes32 requestId) {
        return requestRandomness(keyHash, fee);
    }*/

    /* function loadMap() external {
        body[1] = "Thin";
        body[2] = "Thin";
        body[3] = "Thin";
        body[4] = "Thick";
        body[5] = "Thick";
        body[6] = "Thick";
    } */
}
