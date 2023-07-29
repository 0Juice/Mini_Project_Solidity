pragma solidity ^0.8.0;

contract StudentAttendance {
    struct AttendanceRecord {
        string user;
        string name;
        uint256 timestamp;
        uint32 pid;
        uint64 lectureId;
    }

    mapping (uint32 => mapping (uint64 => AttendanceRecord)) public attendanceRecords;

    function markAttendance(string memory _name, uint32 _pid, uint64 _lectureId) public {
        require(attendanceRecords[_pid][_lectureId].timestamp == 0, "Attendance already marked");
        attendanceRecords[_pid][_lectureId] = AttendanceRecord(_name, block.timestamp, _pid, _lectureId);
    }
}