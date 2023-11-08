CREATE TABLE `plans` (
  `id` bigint(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `max_devices` int(11) NOT NULL,
  `download` int(11) NOT NULL,
  `upload` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `plans`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `plans`
  MODIFY `id` bigint(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;