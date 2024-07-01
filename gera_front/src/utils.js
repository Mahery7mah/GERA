import CryptoJS from 'crypto-js';

const secretKey = '49af716145b3b2dbce1ace42a226fa0cfcddb71f6f6aeeb684111d1f3e5f3025'; // Remplacez par votre propre clé secrète

export function encryptId(id) {
  const encryptedId = CryptoJS.AES.encrypt(id.toString(), secretKey).toString();
  return encodeURIComponent(encryptedId);
}

export function decryptId(encryptedId) {
  const bytes = CryptoJS.AES.decrypt(encryptedId, secretKey);
  return parseInt(bytes.toString(CryptoJS.enc.Utf8));
}