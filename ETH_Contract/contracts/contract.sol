pragma solidity ^0.8.0;

contract Contract{

    struct Desc {
        string updated_by;
        string updated_at;
        string report_hash;
        uint vote_app;
        uint vote_din;
        uint vote_count;
        uint report_index;
    }

    struct Case {
        string created_by;
        string created_at;
        string file_hash;
        mapping(uint256=>Desc) desc;
        string status;
        string description;
    }

    mapping(uint256=>Case) internal cases;

    function createCase(uint256 id, string calldata created_by,  string calldata created_at,  string calldata file_hash, string calldata status, string calldata description) external
    {
        cases[id].created_by = created_by;
        cases[id].created_at = created_at;
        cases[id].file_hash = file_hash;
        cases[id].status = status;
        cases[id].description = description;
    }


    function getCase(uint256 id) external view returns (string memory created_by,
                                                        string memory created_at,
                                                        string memory file_hash,
                                                        string memory status,
                                                        string memory description)
    {
        return (    cases[id].created_by,
                    cases[id].created_at,
                    cases[id].file_hash,
                    cases[id].status,
                    cases[id].description);
    }

    function getLastCaseIndex() external view returns (uint256 index)
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[x].created_at).length  == 0)
                return (x);
        }
    }



    function setNewDescriptor(uint256 id, string calldata updated_by,  string calldata updated_at,  string calldata description,
                              uint256 vote_app,uint256 vote_din, uint256 vote_count, uint256 report_index) external
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                break;
        }
        cases[id].desc[x].updated_by = updated_by;
        cases[id].desc[x].updated_at = updated_at;
        cases[id].desc[x].report_hash = description;
        cases[id].desc[x].vote_app = vote_app;
        cases[id].desc[x].vote_din = vote_din;
        cases[id].desc[x].vote_count = vote_count;
        cases[id].desc[x].report_index = report_index;
    }

    function setoldDescriptor(uint256 id, string calldata updated_by,  string calldata updated_at,  string calldata description,
                              uint256 vote_app,uint256 vote_din, uint256 vote_count, uint256 report_index) external
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                break;
        }
        x -= 1;
        cases[id].desc[x].updated_by = updated_by;
        cases[id].desc[x].updated_at = updated_at;
        cases[id].desc[x].report_hash = description;
        cases[id].desc[x].vote_app = vote_app;
        cases[id].desc[x].vote_din = vote_din;
        cases[id].desc[x].vote_count = vote_count;
        cases[id].desc[x].report_index = report_index;

    }

    function getLastDesc(uint256 id) external view returns (Desc memory)
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                break;
        }
        return (cases[id].desc[x-1]);
    }

    function getLastDescIndex(uint256 id) external view returns (uint256 index)
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                return (x);
        }
    }

    function getDesc(uint256 id, uint256 x) external view returns (Desc memory)
    {
        return (cases[id].desc[x]);
    }

    function setStatus(uint256 id, string calldata status) external
    {
        cases[id].status = status;
    }

    function approve(uint256 id) external
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                break;
        }

        cases[id].desc[x-1].vote_app += 1;
        cases[id].desc[x-1].vote_count += 1;
    }

    function denie(uint256 id) external
    {
        uint x;
        for (x = 0; x != 1000; x += 1)
        {
            if(bytes(cases[id].desc[x].updated_by).length  == 0)
                break;
        }

        cases[id].desc[x-1].vote_din += 1;
        cases[id].desc[x-1].vote_count += 1;
    }
}