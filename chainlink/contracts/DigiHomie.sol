//"SPDX-License-Identifier: UNLICENSED"
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DigiHomie is ERC721, Ownable, AccessControl {
    uint256 public MAX_TOKENS = 5000;
    uint256 public tokenCounter;
    uint256 public mappedCounter;
    string public LOADINGURI;
    bytes32 public constant RESOLVER_ROLE = keccak256("RESOLVER_ROLE");
    //Mapping is store in contract NOT instance
    mapping(uint256 => string) public tokenIdToURI;

    constructor(string memory loadingURI)
        public
        ERC721("DigiHomies", "DH")
        AccessControl()
        Ownable()
    {
        tokenCounter = 0;
        mappedCounter = 0;
        LOADINGURI = loadingURI;
        _setupRole(RESOLVER_ROLE, msg.sender);
    }

    //Creates contract for each homie & sets URI to resolve Homie
    function adminMintHomie(string memory tokenURI)
        public
        onlyOwner
        returns (bytes32)
    {
        require((tokenCounter < MAX_TOKENS), "Exceeds maximum token supply.");
        //Use newItemId and Counter, prior to tokenId via mint
        uint256 newItemId = tokenCounter;

        //URI stored for user Mint
        tokenIdToURI[newItemId] = tokenURI;
        _safeMint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        tokenCounter = tokenCounter + 1;
        mappedCounter = mappedCounter + 1;
    }

    //Creates token
    function adminMintHomiePending(string memory tokenURI)
        public
        onlyOwner
        returns (bytes32)
    {
        require((tokenCounter < MAX_TOKENS), "Exceeds maximum token supply.");

        //Map to track proper URI (not yet used)
        tokenIdToURI[tokenCounter] = tokenURI;
        _safeMint(msg.sender, tokenCounter);
        //Set URI to loading (delayed)
        _setTokenURI(tokenCounter, LOADINGURI);
        tokenCounter = tokenCounter + 1;
        mappedCounter = mappedCounter + 1;
    }

    // Maps to contract tokenIdToURI mapping ahead of token
    function setTokenMapping(string memory tokenURI)
        public
        onlyOwner
        returns (bytes32)
    {
        require((mappedCounter < MAX_TOKENS), "Exceeds maximum token supply.");

        tokenIdToURI[mappedCounter] = tokenURI;
        mappedCounter = mappedCounter + 1;
    }

    //User enabled 'mint' creates token & maps previously assigned tokenIdToURI mapping
    function userMintHomies(uint256 numTokens) public {
        require(
            (tokenCounter + numTokens) < MAX_TOKENS,
            "Exceeds maximum token supply."
        );
        require(
            numTokens > 0 && numTokens <= 10,
            "Minting must be a min of 1 and a max of 10."
        );

        //Iterate numTokens, mint & resolve URI to mapped URI
        for (uint256 i = 0; i < numTokens; i++) {
            //Creates tokenId
            _safeMint(msg.sender, tokenCounter);
            //Set to pre-existing URI and image via folders
            _setTokenURI(tokenCounter, tokenIdToURI[tokenCounter]);
            //Increments token, since token created, mint
            tokenCounter = tokenCounter + 1;
        }
    }

    //Set metadata - Restricted to contract owner
    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require(hasRole(RESOLVER_ROLE, msg.sender), "Caller is not approved.");
        require(_exists(tokenId), "TokenId does not exist");
        _setTokenURI(tokenId, tokenURI);
    }
}
