CREATE TABLE CosmeticsProducts (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_name` VARCHAR(255),
    `website` VARCHAR(250),
    `country` VARCHAR(250),
    `category` VARCHAR(250),
    `subcategory` VARCHAR(250),
    `title_href` VARCHAR(250), -- Cambiado de title-href a title_href
    `price` VARCHAR(250),
    `brand` VARCHAR(250),
    `ingredients` VARCHAR(250),
    `form` VARCHAR(250),
    `type` VARCHAR(250),
    `color` VARCHAR(250),
    `size` VARCHAR(250),
    `rating` VARCHAR(250),
    `noofratings` VARCHAR(250)
);
