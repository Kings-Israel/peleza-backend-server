--
-- Create model BgRequestModule
--
--
-- Create model BusinessCompanyReg
--
--
-- Create model Encumbrance
--
--
-- Create model Module
--
--
-- Create model Package
--
--
-- Create model PackageModule
--
--
-- Create model PSMTRequest
--
--
-- Create model Shares
--
--
-- Create model ShareCapital
--
CREATE TABLE `pel_company_share_capital` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `number_of_shares` varchar(255) NULL, `nominal_value` varchar(255) NULL, `name` varchar(255) NULL, `business_id` integer NULL);
--
-- Create model EncumbranceSecuredAmounts
--
CREATE TABLE `pel_company_secured_amounts` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `currency` varchar(255) NULL, `amount` varchar(255) NULL, `encumbrance_id` bigint NULL);
--
-- Create model EncumbrancePersonsEntitled
--
CREATE TABLE `pel_company_persons_entitled` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NULL, `date_added` datetime(6) NOT NULL, `last_updated` date NOT NULL, `encumbrance_id` bigint NULL);
--
-- Create model CompanyOfficialDetails
--
CREATE TABLE `pel_company_official_details` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `role` varchar(255) NULL, `name` varchar(255) NULL, `date_added` datetime(6) NOT NULL, `last_updated` date NOT NULL, `company_id` integer NOT NULL);
ALTER TABLE `pel_company_share_capital` ADD CONSTRAINT `pel_company_share_ca_business_id_0560e249_fk_pel_compa` FOREIGN KEY (`business_id`) REFERENCES `pel_company_registration` (`company_reg_id`);
ALTER TABLE `pel_company_secured_amounts` ADD CONSTRAINT `pel_company_secured__encumbrance_id_38dccde8_fk_pel_compa` FOREIGN KEY (`encumbrance_id`) REFERENCES `pel_company_encumbrances` (`id`);
ALTER TABLE `pel_company_persons_entitled` ADD CONSTRAINT `pel_company_persons__encumbrance_id_2b28946b_fk_pel_compa` FOREIGN KEY (`encumbrance_id`) REFERENCES `pel_company_encumbrances` (`id`);
ALTER TABLE `pel_company_official_details` ADD CONSTRAINT `pel_company_official_company_id_cf325be8_fk_pel_compa` FOREIGN KEY (`company_id`) REFERENCES `pel_company_registration` (`company_reg_id`);
