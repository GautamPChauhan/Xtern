-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Jun 15, 2025 at 06:40 PM
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

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `email`, `contact_no`, `password`) VALUES
(1, 'Gautam Chauhan', 'chauhangautam176@gmail.com', '8153935673', 'pbkdf2:sha256:1000000$3EqL1emm$5d09e4961e1e8d11c9c5ea77df66afcc4eb3ed287b63c90c24c5a1bef9531d63');

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
(6, 'gautam', 'chauhan', '2005-07-23', '8153935673', 'chauhangautam176@gmail.com', 'Ahmedabad', 'Gujarat', 'pbkdf2:sha256:1000000$3EqL1emm$5d09e4961e1e8d11c9c5ea77df66afcc4eb3ed287b63c90c24c5a1bef9531d63', 'static/resumes\\gautam_gmail_com.pdf'),
(7, 'Aman', 'Vanodiya', '2005-04-16', '6354489913', 'amanmistri45@gmail.com', 'Ahmedabad', 'Gujarat', 'pbkdf2:sha256:1000000$USyFtKym$c6e5ffda721772b8d4a39414a64f9e6bd0c44193e1b8e12b20376e7a933af50a', 'static/resumes\\aman_gmail_com.pdf'),
(8, 'Ruchita', 'Mahale', '2004-09-18', '7359252386', 'ruchi04ta@gmail.com', 'Ahmedabad', 'Gujarat', 'pbkdf2:sha256:1000000$IzRx9MFG4ReVUOBU$39c6a419b8e056192b6f84a72bf902af504d0c9a275d9a85569b3e42723ecaa2', 'static/resumes\\ruchita_gmail_com.pdf'),
(10, 'Aniket', 'Mishra', '2004-12-12', '8153935673', 'aniketmishra0014@gmail.com', 'ahmedabad', 'gujarat', 'pbkdf2:sha256:1000000$QGknw3X23aYPkbfh$307969c28c46d401d5c81f68ca50ef1f439670a6dfd309e2487d3ab86df1c87c', 'static\\resumes\\aniketmishra0014_gmail_com.pdf'),
(11, 'Darshan', 'Virugama', '2004-02-24', '8866630568', 'darshan24204@gmail.com', 'ahmedabad', 'gujarat', 'pbkdf2:sha256:1000000$mDKkbgbe$ac0653e6c436d19611cc62c7016046a5f5ebc1574521728e5cb6a415faf5b427', 'static/resumes\\darshan24204_gmail_com.pdf'),
(13, 'Aagam', 'Jain', '2003-06-01', '8153935673', 'aagamj2004@gmail.com', 'ahmedabad', 'gujarat', 'pbkdf2:sha256:1000000$3ALnKLNEnfzZyAD8$9c6c0585a9bc99f1bd3a1296aaa03c41ce30747f4e01662f74aa682c9e54877d', 'static/resumes\\aagamj2004_gmail_com.pdf'),
(14, 'Hiren', 'Chaudhari', '2003-06-02', '8866630568', 'chaudharihiren2004@gmail.com', 'hyderabad', 'telangana', 'pbkdf2:sha256:1000000$IfMdUuzQmyQIA0HY$dc4824e85efc1eab356ea42c45437862d3c18e168a925287c0cdef392cf5667a', 'static/resumes\\chaudharihiren2004_gmail_com.pdf'),
(15, 'Nirmal', 'Patel', '2002-06-03', '8866630568', 'nirmal140204@gmail.com', 'surat', 'gujarat', 'pbkdf2:sha256:1000000$NYm7BoVHDDd8EQxQ$764b03b4070e122e47563024bb815f31d572871d31fb9566be7fa835f8e57180', 'static/resumes\\nirmal140204_gmail_com.pdf'),
(16, 'Krish', 'patel', '2004-06-06', '8866630568', 'krish1404patel@gmail.com', 'Mumbai', 'Maharashtra', 'pbkdf2:sha256:1000000$rliS6xoIu1Sey6eG$c717bdd34679fdbd38e3cf937e724a69881bb1545f67fe0ff8c12a19596cf411', 'static/resumes\\krish1404patel_gmail_com.pdf'),
(17, 'Deep', 'Kotak', '2004-06-07', '8866630568', 'deepmkotak1103@gmail.com', 'ahmedabad', 'gujarat', 'pbkdf2:sha256:1000000$Gpqsbc4rlSlfogkY$7a0d1673c6d1783109e87130e76fa4176589d943bdc4202d1a92057dba23fa9c', 'static/resumes\\deepmkotak1103_gmail_com.pdf'),
(18, 'Deep', 'Kotak', '2004-06-07', '8866630568', 'deepmkotak1103@gmail.com', 'ahmedabad', 'gujarat', 'pbkdf2:sha256:1000000$rsnmD7gAeklqjZrt$548c1fc2b79e4a41c0a00d85b4f5991d518ae29f05b4b477d0cf2cdd2f3f15da', 'static/resumes\\deepmkotak1103_gmail_com.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `application_id` int(5) NOT NULL,
  `internship_id` int(5) DEFAULT NULL,
  `user_id` int(5) DEFAULT NULL,
  `applied_on` date NOT NULL,
  `status` varchar(15) DEFAULT 'Pending',
  `remarks` varchar(100) DEFAULT NULL,
  `skill_match_percentage` decimal(5,2) DEFAULT NULL,
  `sms_status` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`application_id`, `internship_id`, `user_id`, `applied_on`, `status`, `remarks`, `skill_match_percentage`, `sms_status`) VALUES
(11, 3, 6, '2025-06-11', 'Pending', NULL, 88.89, '2025-06-12 07:04:45'),
(12, 10, 10, '2025-06-11', 'Pending', NULL, 83.33, '2025-06-12 07:04:45'),
(13, 22, 11, '2025-06-14', 'Rejected', NULL, 0.00, '2025-06-14 03:31:57'),
(14, 22, 10, '2025-06-14', 'Pending', NULL, 0.00, '2025-06-14 03:32:54'),
(15, 3, 10, '2025-06-14', 'Pending', NULL, 0.00, '2025-06-14 04:17:55'),
(16, 3, 11, '2025-06-14', 'Rejected', NULL, 0.00, '2025-06-14 04:18:29'),
(17, 3, 11, '2025-06-14', 'Pending', NULL, 11.11, '2025-06-14 04:24:23'),
(18, 8, 17, '2025-06-15', 'Pending', NULL, 0.00, '2025-06-15 16:06:03'),
(19, 10, 17, '2025-06-15', 'Pending', NULL, 50.00, '2025-06-15 16:06:18'),
(20, 9, 17, '2025-06-15', 'Pending', NULL, 66.67, '2025-06-15 16:06:33'),
(21, 22, 14, '2025-06-15', 'Pending', NULL, 40.00, '2025-06-15 16:08:59'),
(22, 23, 14, '2025-06-15', 'Pending', NULL, 40.00, '2025-06-15 16:09:18'),
(23, 28, 14, '2025-06-15', 'Pending', NULL, 20.00, '2025-06-15 16:09:37'),
(24, 30, 15, '2025-06-15', 'Pending', NULL, 50.00, '2025-06-15 16:10:52'),
(25, 12, 15, '2025-06-15', 'Pending', NULL, 50.00, '2025-06-15 16:11:14'),
(26, 23, 16, '2025-06-15', 'Pending', NULL, 40.00, '2025-06-15 16:20:30'),
(27, 22, 16, '2025-06-15', 'Pending', NULL, 80.00, '2025-06-15 16:21:02'),
(28, 7, 7, '2025-06-15', 'Pending', NULL, 66.67, '2025-06-15 16:24:20'),
(29, 26, 7, '2025-06-15', 'Pending', NULL, 16.67, '2025-06-15 16:24:40'),
(30, 14, 7, '2025-06-15', 'Pending', NULL, 16.67, '2025-06-15 16:25:00'),
(31, 26, 8, '2025-06-15', 'Pending', NULL, 50.00, '2025-06-15 16:28:46'),
(32, 7, 8, '2025-06-15', 'Pending', NULL, 44.44, '2025-06-15 16:29:47'),
(33, 11, 11, '2025-06-15', 'Pending', NULL, 16.67, '2025-06-15 16:32:47'),
(34, 22, 11, '2025-06-15', 'Pending', NULL, 0.00, '2025-06-15 16:36:00'),
(35, 27, 13, '2025-06-15', 'Pending', NULL, 50.00, '2025-06-15 16:37:32'),
(36, 14, 13, '2025-06-15', 'Pending', NULL, 16.67, '2025-06-15 16:38:00');

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
(1, 'Tech Innovative', 'techinnovative@gmail.com', 'gautam chauhan', '8153935673', 'https://techinnovative.com', 'Technology', 'Approved', 'pbkdf2:sha256:1000000$0xRfodyk$a69f71a10ccfb8986c263780527cc5f440e54d79ce01caf694e777407652a61b'),
(2, 'Infotech Solutions', 'chauhanpoonam0307@gmail.com', 'Poonam chauhan', '8153935673', 'https://infotechsolutions.com', 'Technology', 'Approved', 'pbkdf2:sha256:1000000$hDSTWNXc6ls53mNo$ffad5228e9b4d6029bf290672170570f4171ce5bf1731a8efb352ec1de118011'),
(3, 'BioGenix Pvt Ltd', 'chauhangautam176@gmail.com', 'Gautam Chauhan', '8153935673', 'https://biogenix.in', 'Biotechnology', 'Approved', 'pbkdf2:sha256:1000000$v3v4nkCrDqOQcjZm$c69b652f4fc5f7c5c0b324f5369b1d2fd6d6d2d51b5f07141116acca23d33fd6'),
(6, 'CodeCraft Technologies Pvt Ltd', 'aniketmishra0014@gmail.com', 'Anjali Mehta', '9099199511', 'https://www.codecraft.in', 'Software Development', 'Approved', 'pbkdf2:sha256:1000000$WDFdAJOyTmi5bkJR$20f3f7355d810b74d8e5ea84a7968352eb582fb60ba1977777949b2510d9fc9c'),
(7, 'GrowthNode Digital', 'darshan24204@gmail.com', 'Rohan Shetty', '9099199511', 'https://www.growthnode.in', 'Digital Marketing', 'Approved', 'pbkdf2:sha256:1000000$nYwJaf9zg2Ln2C3l$401cace8c0b2fed4b8b0020ce494c078f47486b9cf76d0438fef7848bea78b07'),
(8, 'DataGrid Analytics', 'amanmistri45@gmail.com', 'Neha Jain', '9085217305', 'https://www.datagridanalytics.com/', 'Data Science and Analytics', 'Approved', 'pbkdf2:sha256:1000000$azoe3qycZG2AeEbh$4fdf7f738fefbbcbfcfb34ceb604578dc90de978019f48dfb9c05a07b003e312'),
(9, 'PeopleFirst HR Solutions', 'vanodiyaaman25@gmail.com', 'Rajiv Rao', '9825647321', 'https://www.peoplefirsthr.in', 'Human Resource Services', 'Approved', 'pbkdf2:sha256:1000000$I3r7okApXpyJBVWd$1d2462b432d7d159d73492cecef17486811be10d80d73a48650f416f5ddbf64b'),
(10, 'AppForge Labs', 'appforgelabstech@gmail.com', 'Shruti Deshpande', '8754693210', 'https://www.appforgelabs.com', 'Mobile App Development', 'Approved', 'pbkdf2:sha256:1000000$vFQC4EJwffgnU8Kk$cbb8c1935a50a219d81df94556fa19e12c44944f5fde51c9dcfbdecac3517d56'),
(11, 'CreativeInk Studios', 'designcreativeink@gmail.com', 'Karan Patel', '8672135490', 'https://www.creativeink.in', 'Design and Multimedia', 'Pending', 'pbkdf2:sha256:1000000$PpU0IJWAoLWGYNCL$0ba10f431c9c4e2900d738407de079f3caa43d05517b6cced6167264856b5515'),
(12, 'WriteSage Content Solutions', 'writesage@gmail.com', 'Tanvi Malhotra', '8459765320', 'https://www.writesage.com', 'Content Marketing', 'Pending', 'pbkdf2:sha256:1000000$fWbEnzReYwsVtKka$4e07482ac504752bcde97b7cd396d803670318e5a3360d100170a6b1684628d9'),
(13, 'UXFuel Studios', 'uxfueldesign@gmail.com', 'Ajay Narayanan', '9632154870', 'https://www.uxfuel.design', 'UI and UX Design', 'Pending', 'pbkdf2:sha256:1000000$cZEt8cY0zGQGC70K$b21fd9ec11890d235dada86c0b5ded7511fa55de5d271afc4a0d3ddbd083204e'),
(14, 'Secure Layer Seven', 'securelayer7@gmail.com', 'Manoj Srivastava', '8654973210', 'https://www.securelayer7.net', 'Cybersecurity', 'Pending', 'pbkdf2:sha256:1000000$9xDyVAr1YIhMR9Xj$1735c0527cdb8d0a6af5aa2cdf268c3cc6a3201c05a115eda604ce2ea8c71092'),
(15, 'Strat Edge Business Consultants', 'stratedge@gmail.com', 'Devika Kapoor', '7654983210', 'https://www.stratedge.in', 'Business Consulting and Analyt', 'Pending', 'pbkdf2:sha256:1000000$XT6t1lwfQWSdjhSn$cbd34adcc55c320238fcbe3e34aa7b81e4162428285dec5b7041d4421b087e3e');

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
(1, 1, '123, Satyam Mall, Jodhpur Cross Road', 'Jodhpur', 'Ahmedabad', 'Gujarat', '380014', 'Main'),
(2, 2, '123, Satyam Mall, Jodhpur Cross Road', 'Jodhpur', 'Ahmedabad', 'Gujarat', '380014', 'Main'),
(3, 3, '19,pushpakunj society', 'vastral', 'ahmedabad', 'gujarat', '382418', 'Main'),
(5, 6, '3rd Floor, Brigade Tech Park', 'Whitefield', 'Bangalore', 'Karnataka', '560066', 'Main'),
(6, 7, '202, Empire Business Hub', 'Andheri East', 'Mumbai', 'Maharashtra', '400069', 'Main'),
(7, 8, '8th Floor, Worldmark Tower B', 'Aerocity', 'New Delhi', 'Delhi', '110037', 'Main'),
(8, 9, '401, Srinivasa Towers', 'Banjara hills', 'hyderabad', 'telangana', '500034', 'Main'),
(9, 10, '12th Floor, ICC Tech Park', 'senapati bapat road', 'pune', 'Maharashtra', '411016', 'Main'),
(10, 11, '501, Galaxy Business Park', 'Prahladnagar', 'Ahmedabad', 'gujarat', '380015', 'Main'),
(11, 12, 'B-18, Indiranagar 2nd Stage', 'Indiranagar', 'Banglore', 'Karnataka', '560038', 'Main'),
(12, 13, 'No. 77, Ascendas IT Park', 'Taramani', 'Chennai', 'Tamil Nadu', '600113', 'Main'),
(13, 14, 'Tower C, Logix Cyber Park', 'sector 62', 'Noida', 'Uttar pradesh', '201309', 'Main'),
(14, 15, 'Level 5, Vatika Business Centre', 'Sector 44', 'Gurgaon', 'Haryana', '122003', 'Main');

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

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedback_id`, `user_id`, `company_id`, `given_by`, `feedback_text`, `rating`, `date_given`) VALUES
(18, 6, NULL, 'applicant', 'An exellent platform for people having skills , They can get Opportunities as per their skills .😊', 5.0, '2025-06-11 15:08:38'),
(19, NULL, 6, 'company', 'Able to get perfect interns based on their skill match percentage 👍', 4.0, '2025-06-11 15:10:37'),
(20, 6, 6, 'company', 'Hard Working and Curious to learn new things and to help others .', 5.0, '2025-06-11 15:12:03'),
(21, 6, 6, 'applicant', 'Amazing Experience with this Company , skills of interns are valued 😊', 4.0, '2025-06-11 15:14:46'),
(22, 10, NULL, 'applicant', 'Nice Platform 👍', 4.0, '2025-06-11 15:20:17'),
(23, 17, NULL, 'applicant', 'Great user experience ', 4.0, '2025-06-15 21:37:44'),
(24, 13, NULL, 'applicant', 'Perfect platform for finding opportunities', 5.0, '2025-06-15 22:09:32');

-- --------------------------------------------------------

--
-- Table structure for table `internship`
--

CREATE TABLE `internship` (
  `internship_id` int(5) NOT NULL,
  `company_id` int(5) NOT NULL,
  `title` varchar(40) NOT NULL,
  `post` varchar(40) NOT NULL,
  `description` text NOT NULL,
  `duration` varchar(50) NOT NULL,
  `required_skills` text NOT NULL,
  `main_subjects` text NOT NULL,
  `minor_subjects` text NOT NULL,
  `stipend` varchar(15) NOT NULL,
  `location` varchar(100) NOT NULL,
  `remarks` text NOT NULL,
  `internship_status` varchar(7) NOT NULL,
  `open_date` date NOT NULL,
  `close_date` date NOT NULL,
  `status` varchar(7) NOT NULL,
  `job_offer` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `internship`
--

INSERT INTO `internship` (`internship_id`, `company_id`, `title`, `post`, `description`, `duration`, `required_skills`, `main_subjects`, `minor_subjects`, `stipend`, `location`, `remarks`, `internship_status`, `open_date`, `close_date`, `status`, `job_offer`) VALUES
(3, 6, ' React Front-End Development Intern', 'Front-End Developer Intern', 'Work with the front-end development team to design and implement interactive UI components using React.js and modern JavaScript frameworks.', ' 3 Months', 'React.js, HTML5, CSS3, JavaScript, Git', 'Computer Science, Information Technology\r\n\r\n', 'Web Technologies, User Interface Design', '10000/month', 'Bangalore, Karnataka', 'Good performers may receive a Pre-Placement Offer (PPO).', 'open', '2025-06-11', '2025-06-30', 'open', 'Yes'),
(4, 6, 'Software QA & Testing Intern', 'QA Tester Intern', 'Assist in writing and executing test cases, reporting bugs, and performing automated and manual testing of web applications.\r\n\r\n', '2 months', 'Manual Testing, Selenium, Bug Tracking Tools (e.g., JIRA), Basic SQL', 'Software Engineering, Computer Applications', 'Software Testing, Quality Assurance\r\n\r\n', '8000/month', 'Bangalore, Karnataka', 'testing certifications will be considered a plus.', 'open', '2025-06-11', '2025-06-30', 'open', 'No'),
(7, 8, 'Data Science Research Intern', 'Data Scientist Intern', 'Collaborate on ML model development and statistical analysis of large datasets using Python.\r\n\r\n', '4 months', 'Python, Pandas, NumPy, Scikit-learn, SQL\r\n\r\n', 'Data Science, Statistics', 'Machine Learning, Mathematics', '15000/month', 'Remote', 'Research paper opportunities available.', 'open', '2025-06-11', '2025-06-30', 'open', 'Yes'),
(8, 8, 'Business Intelligence Intern', 'BI Developer Intern', 'Design dashboards and prepare data visualizations using Power BI and Tableau.', '3 months', 'Power BI, SQL, Excel, Data Interpretation', ' Business Analytics', 'Data Visualization, MIS Reporting', '10000/month', 'Remote', 'Strong Excel skills essential.', 'open', '2025-06-14', '2025-06-30', 'open', 'No'),
(9, 9, 'Recruitment Intern', ' Talent Acquisition Intern', 'Assist in resume screening, scheduling interviews, and maintaining applicant data.', '2 months', 'Communication, MS Excel, ATS familiarity\r\n\r\n', 'Human Resources', 'Organizational Behavior, Business Administration', '6000/month', 'hyderabad,Telangana', 'PPO for high performers', 'open', '2025-06-11', '2025-06-30', 'open', 'Yes'),
(10, 9, 'HR Operations Intern', 'HR Coordinator Intern', 'Help with documentation, onboarding, leave tracking, and policy updates.\r\n\r\n', '3 months', 'Excel, Documentation, HRMS software', 'HR Management', 'Corporate Law, Labor Relations', '7000/month', 'hyderabad,Telangana', 'Opportunity to work with senior HR managers.\r\n\r\n', 'open', '2025-06-11', '2025-06-30', 'open', 'Yes'),
(11, 6, 'Web Development Intern', 'Front-End Developer', 'Assist in designing user interfaces for client websites using HTML, CSS, and JavaScript.', '3 Months', 'HTML5, CSS3, JavaScript, Bootstrap', 'Computer Science', 'Web Technologies', '8,000/month', 'Remote', 'Must complete 1 portfolio project', 'open', '2025-06-13', '2025-06-30', 'open', 'No'),
(12, 1, 'Cloud Computing Intern', 'Cloud Infrastructure Intern', 'Work with the DevOps team to set up scalable environments on AWS', '4 Months', 'AWS, Docker, CI/CD, Linux', 'Cloud Computing', 'Networking', '12,000/month', 'Bengaluru, Karnataka', 'AWS certified preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(13, 1, 'UI/UX Design Intern', 'UI/UX Intern', 'Design user-centric interfaces and wireframes for web apps.', '3 Months', 'Figma, Adobe XD, UX principles, Prototyping', 'User Experience Design', 'Human-Computer Interaction', '8,500/month', 'Bengaluru (Hybrid)', 'Portfolio link required', 'open', '2025-06-14', '2025-06-30', 'open', 'Yes'),
(14, 2, 'Python Developer Intern', 'Backend Developer Intern', ' Assist in developing APIs and backend logic for web applications using Python and Flask.', '3 Months', 'Python, Flask, REST APIs, Git', 'Information Technology', 'Backend Systems', '9,000/month', 'Mumbai, Maharashtra', 'Final year students preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(15, 2, 'Data Entry & QA Intern', 'Data Entry & Tester', 'Perform manual testing and validate data entry operations for internal applications.', '2 Months', 'Excel, Manual Testing, Attention to detail', 'Computer Applications', 'Quality Assurance', '6,000/month', 'Remote', 'Certification provided', 'open', '2025-06-15', '2025-06-30', 'open', 'Yes'),
(16, 2, 'IT Support & Networking Intern', 'Network Support Intern', 'Provide tech support and assist in configuring LAN/WAN setups.', '2 Months', 'Networking Basics, Troubleshooting, Windows/Linux OS', 'Computer Networks', 'IT Infrastructure', '7,000/month', 'Mumbai (On-site)', 'Basic hardware knowledge preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(17, 3, 'Research Intern – Molecular Biology', 'Molecular Biology Research Intern', 'Support ongoing research involving DNA sequencing and cell culture techniques.', '4 Months', 'PCR, Gel Electrophoresis, Research Documentation', 'Biotechnology', 'Microbiology', '10,000/month', 'Pune, Maharashtra', 'Lab coat & safety training provided', 'open', '2025-06-15', '2025-06-30', 'open', 'Yes'),
(18, 3, 'Bioinformatics Intern', 'Bioinformatics Analyst', 'Analyze genomic datasets and run simulations using software tools.', '3 Months', 'Python/R, BLAST, BioPython, Data Cleaning', 'Bioinformatics', 'Computational Biology', '9,000/month', 'Remote', 'Must know basic programming', 'open', '2025-06-14', '2025-06-30', 'open', 'Yes'),
(19, 3, 'Clinical Data Analyst Intern', 'Clinical Research Intern', 'Analyze clinical trial data for consistency and prepare summary reports.', '3 Months', 'SPSS, Excel, Clinical Research Basics, Statistics', 'Life Sciences', 'Biostatistics', '8,000/month', 'Pune (On-site)', 'Preferred candidates from B.Pharm/B.Sc background', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(21, 6, 'Full Stack Developer Intern', 'Full Stack Developer', 'Work on both front and back-end modules using MERN stack.', ' 4 Months', 'Node.js, MongoDB, Express.js, React', 'Computer Science', ' Backend Systems', '12,000/month', 'Bangalore, Karnataka', 'Real-world project experience', 'open', '2025-06-13', '2025-06-30', 'open', 'No'),
(22, 7, 'Social Media Marketing Intern', 'SMM Intern', 'Plan and create content for Instagram, Facebook, LinkedIn.', '3 Months', 'Canva, Meta Suite, Copywriting', 'Marketing', 'Digital Media', '7,000/month', 'Mumbai, Maharashtra', 'Work on real client accounts', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(23, 7, 'SEO Analyst Intern', 'SEO Intern', 'Optimize website content for search engines.', '2 Months', 'SEO Tools, Google Search Console, SEMrush', 'Marketing', 'Analytics', '6,000/month', 'Mumbai, Maharashtra', 'Certificate of completion', 'open', '2025-06-13', '2025-06-30', 'open', 'No'),
(24, 7, 'Email Campaign Intern', 'Email Marketing Intern', 'Design and deliver email campaigns; analyze open rates and A/B test subject lines.', '2 Months', 'Mailchimp, HTML Email, Design Basics, Excel', 'Marketing', 'Data Analytics', '6,500/month', 'Mumbai (Hybrid)', 'Good copywriting skills helpful', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(25, 7, 'PPC Campaign Intern', 'PPC Intern', 'Monitor and optimize Google Ads and social media paid campaigns to maximize ROI.', '3 Months', 'Google Ads, Analytics, Budgeting, Excel', 'Advertising', 'Business Analytics', '8000/month', 'Mumbai', 'Google Ads certification preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(26, 8, 'NLP Research Intern', 'NLP Intern', 'Implement NLP models for sentiment analysis using Python and spaCy/NLTK.', '4 Months', 'Python, NLTK, Text Mining, SQL', 'Natural Language Processing', 'Linguistics', '15000/month', 'Remote', 'ML project experience preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(27, 8, 'Predictive Modeling Intern', 'Predictive Analytics Intern', 'Build and validate predictive models using regression and classification techniques.', '3 Months', 'Python, Scikit‑Learn, Pandas, Data Cleaning', 'Statistics', 'Machine Learning', '12,000/month', 'Remote', 'Kaggle participation is a plus', 'open', '2025-06-13', '2025-06-30', 'open', 'No'),
(28, 9, 'Employer Branding Intern', 'HR Marketing Intern', 'Develop employer brand content for social media and internal platforms.', '3 Months', 'Social Media, Content Writing, Communication', 'HR Management', 'Marketing', '7,500/month', 'Hyderabad, Telangana', 'Graphic design basics helpful', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(29, 9, 'L&D Intern', 'Support training session design and inte', 'MS PowerPoint, Facilitation Skills, Content Curation', '3 Months', 'MS PowerPoint, Facilitation Skills, Content Curation', 'Organizational Behavior', 'Adult Learning', '8,000/month', 'Hyderabad, Telangana', 'Must assist in at least one workshop', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(30, 10, 'Flutter UI Intern', 'Flutter UI Developer', 'Create visually appealing Flutter UI components based on design mockups.', '3 Months', 'Flutter, Dart, UI Integration, Git', 'Mobile Computing', 'UI Design', '11,000/month', 'Pune, Maharashtra', 'Design-to-code experience preferred', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes'),
(31, 10, 'Mobile QA Intern', 'Mobile QA Intern', 'Write automated tests for Android/iOS apps and log bug reports.', '3 Months', 'Appium, Java/Kotlin, TestNG', 'Software Testing', 'Mobile App Testing', '10,000/month', 'Pune', 'Mobile testing certification a bonus', 'open', '2025-06-13', '2025-06-30', 'open', 'Yes');

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
(1, 6, 1, '2021', 'Gujarat Board', 87.00, 'Maths,Science,English', 'Computer,English', 'HTML,CSS,Python', 'Python Developer', 'Don Bosco English School'),
(2, 8, 4, '2024', 'Gujarat University', 87.00, 'Artificial Intelligence, Machine Learning', 'Mathemetics', 'Python, Pandas, NumPy, NLTK, Text Mining', 'AI, Robotics, UI Design', 'Department of Computer Science'),
(9, 11, 1, '2024', 'Gujarat University', 60.00, 'Web Development', 'SE', 'HTML, CSS, JS ,Frontend', 'Development', 'Department of computer science'),
(10, 6, 4, '2025', 'Gujarat University', 87.00, 'Computer Science, Information Technology', 'Web Technologies, User Interface Design', 'React.js, HTML5, CSS3, JavaScript', 'Gymming , Music', 'Department of computer science'),
(11, 10, 7, '2025', 'Gujarat University', 80.00, 'HR Management, Finance', 'Corporate Law, Labour Relations', 'Excel, Documentation, HRMS Software', 'Music, Running, Socializing', 'B.K School of Business Management'),
(12, 11, 9, '2025', 'GTU', 70.00, 'web Development', 'SEO', 'HTML5, CSS, React', 'Designing', 'LD Engineering College'),
(13, 13, 4, '2024', 'Gujarat University', 80.00, 'Computer science', 'Machine learning', 'Python, Pandas, NumPy', 'Exploring new technologies', 'Department of computer science'),
(14, 14, 7, '2025', 'Gujarat University', 70.00, 'Marketing', 'Digital Media, Business Analytics', 'Google Ads, Excel, SEO Tools, ', 'Content writing ', 'B.K School of Business Management'),
(15, 15, 4, '2024', 'Gujarat Technological University', 75.00, 'App development, cloud computing', 'software engineering', 'Flutter, Dart, UI Integration, AWS, Docker', 'Music', 'LD Engineering College'),
(16, 17, 7, '2025', 'Gujarat University', 80.00, 'Human Resources', 'Organizational Behavior, Labor Relations', 'Documentation, HRMS software, Communication, MS Excel', 'Communicating with people and helping them', 'K.S. School of business management'),
(17, 16, 3, '2024', 'Ahmedabad University', 78.00, 'Marketing , Graphics Designing', 'content writing', 'Canva, Meta Suite, Copywriting, SEO Tools,', 'Designing', 'Department of Social Marketing'),
(18, 7, 9, '2025', 'Gujarat University', 65.00, 'Data Science, Statistics', 'Machine Learning', 'Python, Pandas, NumPy, ', 'Reading Books', 'Department of computer science');

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
  ADD PRIMARY KEY (`user_id`);

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
  MODIFY `admin_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `applicant`
--
ALTER TABLE `applicant`
  MODIFY `user_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `application_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `company_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `company_address`
--
ALTER TABLE `company_address`
  MODIFY `address_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `degree`
--
ALTER TABLE `degree`
  MODIFY `degree_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `feedback_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `internship`
--
ALTER TABLE `internship`
  MODIFY `internship_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `user_qualification`
--
ALTER TABLE `user_qualification`
  MODIFY `qualification_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

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
