-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Apr 23, 2025 at 06:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `internship_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(5) NOT NULL,
  `admin_name` varchar(30) NOT NULL,
  `email` varchar(60) NOT NULL,
  `contact_no` varchar(13) NOT NULL,
  `password` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `applicant`
--

CREATE TABLE `applicant` (
  `user_id` int(5) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `dob` date NOT NULL,
  `contact_no` varchar(13) NOT NULL,
  `email` varchar(60) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `password` varchar(500) NOT NULL,
  `resume_url` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applicant`
--

INSERT INTO `applicant` (`user_id`, `fname`, `lname`, `dob`, `contact_no`, `email`, `city`, `state`, `password`, `resume_url`) VALUES
(6, 'gautam', 'chauhan', '2005-07-23', '8153935673', 'gautam@gmail.com', 'Ahmedabad', 'Gujarat', 'pbkdf2:sha256:1000000$2Vj0BjDnLrjbNeb2$3c4e0fb8d7d6fa66a9b8828e755d12e13237b15a005a3732250b0d55e2d07429', 'static/resumes\\gautam_gmail_com.pdf'),
(7, 'Aman', 'Vanodiya', '2005-04-16', '6354489913', 'aman@gmail.com', 'Ahmedabad', 'Gujarat', 'pbkdf2:sha256:1000000$RoAR5FgepjyxGP2Q$0df794a1c1f4044c5f4a7e54169991b33231af26de0281f87140149de247392e', 'static/resumes\\aman_gmail_com.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `application_id` int(5) NOT NULL,
  `internship_id` int(5) DEFAULT NULL,
  `user_id` int(5) DEFAULT NULL,
  `applied_on` date NOT NULL,
  `status` varchar(100) DEFAULT 'Pending',
  `remarks` varchar(100) DEFAULT NULL,
  `skill_match_percentage` decimal(5,2) DEFAULT NULL,
  `sms_status` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`application_id`, `internship_id`, `user_id`, `applied_on`, `status`, `remarks`, `skill_match_percentage`, `sms_status`) VALUES
(1, 1, 6, '2025-04-23', 'Withdrawn', NULL, 18.18, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `company_id` int(5) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `email` varchar(60) NOT NULL,
  `contact_person` varchar(30) NOT NULL,
  `contact_no` varchar(13) NOT NULL,
  `website_url` text NOT NULL,
  `industry` varchar(30) NOT NULL,
  `status` varchar(15) NOT NULL DEFAULT 'Pending',
  `password` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`company_id`, `company_name`, `email`, `contact_person`, `contact_no`, `website_url`, `industry`, `status`, `password`) VALUES
(1, 'Tech Innovative', 'techinnovative@gmail.com', 'gautam chauhan', '8153935673', 'https://techinnovative.com', 'Technology', 'Approved', 'pbkdf2:sha256:1000000$PsZXx4cEq70dhCVA$738d77abc0e03fb1c548f2b45fabfbf98262521cb3c8cc531945c9e6fb406608');

-- --------------------------------------------------------

--
-- Table structure for table `company_address`
--

CREATE TABLE `company_address` (
  `address_id` int(5) NOT NULL,
  `company_id` int(5) NOT NULL,
  `address_line` varchar(80) NOT NULL,
  `area` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `pincode` varchar(6) NOT NULL,
  `address_type` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company_address`
--

INSERT INTO `company_address` (`address_id`, `company_id`, `address_line`, `area`, `city`, `state`, `pincode`, `address_type`) VALUES
(1, 1, '123, Satyam Mall, Jodhpur Cross Road', 'Jodhpur', 'Ahmedabad', 'Gujarat', '380014', 'Main');

-- --------------------------------------------------------

--
-- Table structure for table `degree`
--

CREATE TABLE `degree` (
  `degree_id` int(5) NOT NULL,
  `degree_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `degree`
--

INSERT INTO `degree` (`degree_id`, `degree_name`) VALUES
(1, '10th'),
(2, '12th'),
(8, 'B.Com'),
(9, 'B.Tech'),
(6, 'BA'),
(7, 'BBA'),
(5, 'BCA'),
(4, 'BSc'),
(3, 'Diploma'),
(14, 'M.Com'),
(15, 'M.Tech'),
(12, 'MA'),
(13, 'MBA'),
(11, 'MCA'),
(10, 'MSc');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `feedback_id` int(5) NOT NULL,
  `user_id` int(5) DEFAULT NULL,
  `company_id` int(5) DEFAULT NULL,
  `given_by` enum('applicant','company','admin') NOT NULL,
  `feedback_text` text NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `date_given` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `internship`
--

CREATE TABLE `internship` (
  `internship_id` int(5) NOT NULL,
  `company_id` int(5) NOT NULL,
  `title` varchar(30) NOT NULL,
  `post` varchar(30) NOT NULL,
  `description` text NOT NULL,
  `duration` varchar(50) NOT NULL,
  `required_skills` text NOT NULL,
  `main_subjects` text NOT NULL,
  `minor_subjects` text NOT NULL,
  `stipend` varchar(15) NOT NULL,
  `location` varchar(100) NOT NULL,
  `remarks` text NOT NULL,
  `internship_status` varchar(6) NOT NULL,
  `open_date` date NOT NULL,
  `close_date` date NOT NULL,
  `status` varchar(5) NOT NULL,
  `job_offer` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `internship`
--

INSERT INTO `internship` (`internship_id`, `company_id`, `title`, `post`, `description`, `duration`, `required_skills`, `main_subjects`, `minor_subjects`, `stipend`, `location`, `remarks`, `internship_status`, `open_date`, `close_date`, `status`, `job_offer`) VALUES
(1, 1, 'Software Development Intern', 'Full Stack Developer Intern', 'Join our development team to build scalable web applications using modern technologies. You’ll be working under experienced mentors and will contribute to real-time projects.', '3 months', 'HTML, CSS, JavaScript, React.js, Node.js, MySQL\r\n', 'Web Development, Software Engineering, Database Systems\r\n', 'UI/UX Design, Cloud Computing', '8000/month', 'Ahmedabad, Gujarat', 'Remote work option available; high-performing interns may be offered a full-time position.', 'Open', '2025-04-22', '2025-05-10', 'Open', 'Yes');

-- --------------------------------------------------------

--
-- Table structure for table `user_qualification`
--

CREATE TABLE `user_qualification` (
  `qualification_id` int(5) NOT NULL,
  `user_id` int(5) DEFAULT NULL,
  `degree_id` int(5) DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `board` varchar(50) DEFAULT NULL,
  `percentage` decimal(5,2) DEFAULT NULL,
  `main_subjects` text DEFAULT NULL,
  `sub_subjects` text DEFAULT NULL,
  `skills` text DEFAULT NULL,
  `interest` text DEFAULT NULL,
  `institute` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_qualification`
--

INSERT INTO `user_qualification` (`qualification_id`, `user_id`, `degree_id`, `year`, `board`, `percentage`, `main_subjects`, `sub_subjects`, `skills`, `interest`, `institute`) VALUES
(1, 6, 1, '2020', 'Gujarat Board', 77.00, 'Maths,Science,English', 'Computer,English', 'HTML,CSS,Python', 'Python Developer', 'Don Bosco English School');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `applicant`
--
ALTER TABLE `applicant`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`application_id`),
  ADD KEY `fk5` (`internship_id`),
  ADD KEY `fk6` (`user_id`);

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`company_id`);

--
-- Indexes for table `company_address`
--
ALTER TABLE `company_address`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `fk` (`company_id`);

--
-- Indexes for table `degree`
--
ALTER TABLE `degree`
  ADD PRIMARY KEY (`degree_id`),
  ADD UNIQUE KEY `degree_name` (`degree_name`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `company_id` (`company_id`);

--
-- Indexes for table `internship`
--
ALTER TABLE `internship`
  ADD PRIMARY KEY (`internship_id`),
  ADD KEY `fk4` (`company_id`);

--
-- Indexes for table `user_qualification`
--
ALTER TABLE `user_qualification`
  ADD PRIMARY KEY (`qualification_id`),
  ADD KEY `fk2` (`user_id`),
  ADD KEY `fk3` (`degree_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `applicant`
--
ALTER TABLE `applicant`
  MODIFY `user_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `application_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `company_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `company_address`
--
ALTER TABLE `company_address`
  MODIFY `address_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `degree`
--
ALTER TABLE `degree`
  MODIFY `degree_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `internship`
--
ALTER TABLE `internship`
  MODIFY `internship_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_qualification`
--
ALTER TABLE `user_qualification`
  MODIFY `qualification_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `fk5` FOREIGN KEY (`internship_id`) REFERENCES `internship` (`internship_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk6` FOREIGN KEY (`user_id`) REFERENCES `applicant` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `company_address`
--
ALTER TABLE `company_address`
  ADD CONSTRAINT `fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `applicant` (`user_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`) ON DELETE SET NULL;

--
-- Constraints for table `internship`
--
ALTER TABLE `internship`
  ADD CONSTRAINT `fk4` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_qualification`
--
ALTER TABLE `user_qualification`
  ADD CONSTRAINT `fk2` FOREIGN KEY (`user_id`) REFERENCES `applicant` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk3` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`degree_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
