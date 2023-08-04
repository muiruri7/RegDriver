-- phpMyAdmin SQL Dump
-- version 5.2.1-1.fc38
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 04, 2023 at 04:23 PM
-- Server version: 10.5.21-MariaDB
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `registration`
--

-- --------------------------------------------------------

--
-- Table structure for table `2nk_sacco`
--

CREATE TABLE `2nk_sacco` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `4nte_sacco`
--

CREATE TABLE `4nte_sacco` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `name` varchar(100) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `license` varchar(20) DEFAULT NULL,
  `national_id` varchar(20) DEFAULT NULL,
  `license_plate_number` varchar(20) DEFAULT NULL,
  `organization` varchar(100) DEFAULT NULL,
  `vehicle_classification` varchar(50) DEFAULT NULL,
  `vehicle_model` varchar(50) DEFAULT NULL,
  `route_number` varchar(50) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`name`, `gender`, `mobile_number`, `license`, `national_id`, `license_plate_number`, `organization`, `vehicle_classification`, `vehicle_model`, `route_number`, `id`) VALUES
('Maina Kavani', 'male', '072345678', '12321', '1234567', 'KAE 765R', 'Super Metro', 'Bus', 'Isuzu', '101', 1);

-- --------------------------------------------------------

--
-- Table structure for table `lopha_travellers`
--

CREATE TABLE `lopha_travellers` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `lopha_travellers`
--

INSERT INTO `lopha_travellers` (`license_plate_number`, `vehicle_classification`, `vehicle_model`, `driver_status`, `route_number`) VALUES
('KAE 765R', 'Bus', 'Isuzu', 'Active', 101),
('KAG 2109', 'Matatu', 'Nissan', 'Active', 102),
('KBD 987M', 'Bus', 'Scania', 'Inactive', 103),
('KBF 6543', 'Matatu', 'Toyota', 'Active', 104),
('KCA 543W', 'Bus', 'Volvo', 'Active', 105),
('KCB 321Y', 'Matatu', 'Mitsubishi', 'Inactive', 106),
('KAD 987E', 'Bus', 'Isuzu', 'Active', 107),
('KAF 765R', 'Matatu', 'Nissan', 'Active', 108),
('KBG 543Q', 'Bus', 'Scania', 'Inactive', 109),
('KCH 321P', 'Matatu', 'Toyota', 'Active', 110),
('KAD 987O', 'Bus', 'Volvo', 'Active', 111),
('KAF 765N', 'Matatu', 'Mitsubishi', 'Inactive', 112),
('KBG 543M', 'Bus', 'Isuzu', 'Active', 113),
('KCH 321L', 'Matatu', 'Nissan', 'Active', 114),
('KAD 987J', 'Bus', 'Scania', 'Inactive', 115),
('KAF 765H', 'Matatu', 'Toyota', 'Active', 116),
('KBG 543G', 'Bus', 'Volvo', 'Active', 117),
('KCH 321F', 'Matatu', 'Mitsubishi', 'Inactive', 118),
('KAD 987E', 'Bus', 'Isuzu', 'Active', 119),
('KAF 765R', 'Matatu', 'Nissan', 'Active', 120),
('KBG 543Q', 'Bus', 'Scania', 'Inactive', 121),
('KCH 321P', 'Matatu', 'Toyota', 'Active', 122);

-- --------------------------------------------------------

--
-- Table structure for table `manchester_travellers`
--

CREATE TABLE `manchester_travellers` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `manchester_travellers`
--

INSERT INTO `manchester_travellers` (`license_plate_number`, `vehicle_classification`, `vehicle_model`, `driver_status`, `route_number`) VALUES
('KAE 6543', 'Bus', 'Isuzu', 'Active', 101),
('KAC 3210', 'Matatu', 'Nissan', 'Active', 102),
('KGB 543Q', 'Bus', 'Scania', 'Inactive', 103),
('KCH 765R', 'Matatu', 'Toyota', 'Active', 104),
('KAD 987E', 'Bus', 'Volvo', 'Active', 105),
('KAF 321P', 'Matatu', 'Mitsubishi', 'Inactive', 106),
('KBG 987O', 'Bus', 'Isuzu', 'Active', 107),
('KAF 765H', 'Matatu', 'Nissan', 'Active', 108),
('KBG 8765', 'Bus', 'Scania', 'Inactive', 109),
('KCH 765P', 'Matatu', 'Toyota', 'Active', 110),
('KAD 987G', 'Bus', 'Volvo', 'Active', 111),
('KAF 987N', 'Matatu', 'Mitsubishi', 'Inactive', 112),
('KBG 4321', 'Bus', 'Isuzu', 'Active', 113),
('KCH 543L', 'Matatu', 'Nissan', 'Active', 114),
('KAD 765J', 'Bus', 'Scania', 'Inactive', 115),
('KAF 321F', 'Matatu', 'Toyota', 'Active', 116),
('KBG 987Q', 'Bus', 'Volvo', 'Active', 117),
('KCH 765G', 'Matatu', 'Mitsubishi', 'Inactive', 118),
('KAD 987E', 'Bus', 'Isuzu', 'Active', 119),
('KAF 765R', 'Matatu', 'Nissan', 'Active', 120),
('KBG 543Q', 'Bus', 'Scania', 'Inactive', 121),
('KCH 321P', 'Matatu', 'Toyota', 'Active', 122);

-- --------------------------------------------------------

--
-- Table structure for table `naekana_sacco`
--

CREATE TABLE `naekana_sacco` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `neo_kenya_kenya_sacco`
--

CREATE TABLE `neo_kenya_kenya_sacco` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roster`
--

CREATE TABLE `roster` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `clock_in` datetime DEFAULT NULL,
  `clock_out` datetime DEFAULT NULL,
  `pickup_point` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `route_number` varchar(50) DEFAULT NULL,
  `driver_status` varchar(20) DEFAULT NULL,
  `reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `pickup_point` text NOT NULL,
  `destination` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`pickup_point`, `destination`, `route_number`) VALUES
('City Stadium', 'Thika Road', 34),
('Kenyatta National Hospital', 'Westlands', 44),
('Ngong Railway Station', 'Ongata Rongai', 12),
('Mwiki Market', 'Kikuyu', 104),
('Kangemi', 'Kawangware', 111),
('Donholm Estate', 'Karen', 144),
('Embakasi Bus Station', 'Ruiru', 24),
('Imara Daima', 'Kithengela', 84),
('Kayole Market', 'Komarock', 94),
('Juja Town', 'Ruiru', 54),
('Utawala', 'Athi River', 64),
('Kikuyu', 'Limuru', 74),
('Ongata Rongai', 'Narok', 102),
('Ngong Town', 'Kajiado', 112),
('Kawangware', 'Kahawa Wendani', 121),
('Dagoretti', 'Kiambu Town', 134),
('Kithengela', 'Namanga', 142),
('Komarock', 'Thika', 154),
('Karen', 'Lang\'ata', 164),
('Limuru', 'Mwea', 174),
('Athi River', 'Machakos', 184),
('Ruiru', 'Naivasha', 194),
('Thika', 'Muranga', 204),
('Embu', 'Meru', 214),
('Nanyuki', 'Isiolo', 224),
('Nyeri', 'Karatina', 234),
('Muranga', 'Murang\'a Town', 244),
('Kirinyaga', 'Sagana', 254),
('Kiambu', 'Gatundu', 264),
('Machakos', 'Yatta', 274),
('Kitui', 'Mwingi', 284),
('Mombasa', 'Voi', 294),
('Malindi', 'Lamu', 304),
('Kisumu', 'Kakamega', 314),
('Bungoma', 'Busia', 324),
('Eldoret', 'Kitale', 334),
('Nakuru', 'Kericho', 344),
('Naivasha', 'Narok', 354);

-- --------------------------------------------------------

--
-- Table structure for table `super_metro`
--

CREATE TABLE `super_metro` (
  `license_plate_number` varchar(10) NOT NULL,
  `vehicle_classification` text NOT NULL,
  `vehicle_model` varchar(20) NOT NULL,
  `driver_status` text NOT NULL,
  `route_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `super_metro`
--

INSERT INTO `super_metro` (`license_plate_number`, `vehicle_classification`, `vehicle_model`, `driver_status`, `route_number`) VALUES
('KAE 765R', 'Bus', 'Isuzu', 'Active', 101),
('KAG 2109', 'Matatu', 'Nissan', 'Active', 102),
('KBD 987M', 'Bus', 'Scania', 'Inactive', 103),
('KBF 6543', 'Matatu', 'Toyota', 'Active', 104),
('KCA 543W', 'Bus', 'Volvo', 'Active', 105),
('KCB 321Y', 'Matatu', 'Mitsubishi', 'Inactive', 106),
('KAD 987E', 'Bus', 'Isuzu', 'Active', 107),
('KAF 765R', 'Matatu', 'Nissan', 'Active', 108),
('KBG 543Q', 'Bus', 'Scania', 'Inactive', 109),
('KCH 321P', 'Matatu', 'Toyota', 'Active', 110),
('KAD 987O', 'Bus', 'Volvo', 'Active', 111),
('KAF 765N', 'Matatu', 'Mitsubishi', 'Inactive', 112),
('KBG 543M', 'Bus', 'Isuzu', 'Active', 113),
('KCH 321L', 'Matatu', 'Nissan', 'Active', 114),
('KAD 987J', 'Bus', 'Scania', 'Inactive', 115),
('KAF 765H', 'Matatu', 'Toyota', 'Active', 116),
('KBG 543G', 'Bus', 'Volvo', 'Active', 117),
('KCH 321F', 'Matatu', 'Mitsubishi', 'Inactive', 118),
('KAD 987E', 'Bus', 'Isuzu', 'Active', 119),
('KAF 765R', 'Matatu', 'Nissan', 'Active', 120),
('KBG 543Q', 'Bus', 'Scania', 'Inactive', 121),
('KCH 321P', 'Matatu', 'Toyota', 'Active', 122);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', '123456', 'admin'),
(2, 'Leon', '708090', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roster`
--
ALTER TABLE `roster`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `drivers`
--
ALTER TABLE `drivers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `roster`
--
ALTER TABLE `roster`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
