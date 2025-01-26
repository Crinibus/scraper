import { ProductInfo } from "../pages/ProductsPage";

// TODO: Get products from API
export const products: ProductInfo[] = [
  { id: "1", name: "Logitech Z533", category: "Speaker", domain: "Proshop", currency: "DKK", isActive: true },
  { id: "2", name: "Google Pixel 9", category: "Phone", domain: "Komplett", currency: "DKK", isActive: true },
  { id: "3", name: "Keycron K10", category: "Keyboard", domain: "ComputerSalg", currency: "DKK", isActive: false },
];

export const randomPrice = (upperLimit: number) => {
  return Math.floor(Math.random() * upperLimit);
};
