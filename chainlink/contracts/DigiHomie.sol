pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DigiHomie is ERC721, Ownable {
    uint256 public MAX_TOKENS = 25000;
    uint256 public tokenPrice = 10000000000000000; //.01 Eth
    uint256 public tokenCounter;
    mapping(uint256 => string) public tokenIdToURI;

    constructor() public ERC721("DigiHomies", "DH") {
        tokenCounter = 0;
    }

    //Creates contract for each homie & sets URI to resolve Homie
    function mintHomie(string memory tokenURI)
        public
        onlyOwner
        returns (bytes32)
    {
        //Use newItemId and Counter, prior to tokenId via mint
        uint256 newItemId = tokenCounter;
        address homieOwner = msg.sender;

        //URI stored for user Mint
        tokenIdToURI[newItemId] = tokenURI;
        _safeMint(homieOwner, newItemId);
        setTokenURI(newItemId, tokenURI);

        tokenCounter = tokenCounter + 1;
    }

    //UserMint - allow user to create new (resolve URI)
    function userMintHomies(uint256 numTokens) public payable {
        require(
            SafeMath.add(totalSupply(), numTokens) <= MAX_TOKENS,
            "Exceeds maximum token supply."
        );
        require(
            numTokens > 0 && numTokens <= 10,
            "Minting must be a min of 1 and a max of 10."
        );
        require(
            msg.value >= SafeMath.mul(calculatePrice(), numTokens),
            "Amount of Ether sent is not correct."
        );

        //Iterate numTokens, mint & resolve URI to mapped URI
        for (uint256 i = 0; i < numTokens; i++) {
            uint256 mintIndex = totalSupply();
            _safeMint(msg.sender, mintIndex);
            setTokenURI(mintIndex, tokenIdToURI[mintIndex]);
        }
    }

    function calculatePrice() public view returns (uint256) {
        require(totalSupply() < MAX_TOKENS, "No more tokens");
        return tokenPrice; // 0.1 ETH
    }

    //Set metadata - Restricted to contract owner
    function setTokenURI(uint256 tokenId, string memory _tokenURI)
        public
        onlyOwner
    {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner or approved."
        );
        require(_exists(tokenId), "TokenId does not exist");
        //Set Mapping
        tokenIdToURI[tokenId] = _tokenURI;
        //Set with Homie mapping (resolve proper URI)
        _setTokenURI(tokenId, _tokenURI);
    }

    function getTokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId));
        return tokenIdToURI[tokenId];
    }
}
