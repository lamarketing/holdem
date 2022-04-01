import {postZ} from "@/api/axios";

const setTokenL = (token: string) => localStorage.setItem('token', token)
const removeTokenL = () => localStorage.removeItem('token')
const getTokenL = () => localStorage.getItem('token')

/**
 * Получение токена с сервера по логину и паролю
 */
async function getToken(username: string, password: string) {
  removeTokenL()
  const token = await postZ('token',{username: username, password: password})

  return token ? token.token : null
}

async function isAuth(username: string, password: string) {
  let token: string | null = getTokenL()
  if (!token) {
    token = await getToken(username, password)
    console.log(token)
    if (token) {
      setTokenL(token)
    }
    return !!token;
  }
  token = await getToken(username, password)
  if (token) {
    setTokenL(token)
  } else {
    removeTokenL()
  }

  return !!token
}

export {
  getToken,
  setTokenL,
  removeTokenL,
  getTokenL,
  isAuth
}