import {getZ} from "@/api/axios";

const tournament_url = 'tournaments'

/**
 * Список всех ожидаемых турниров.
 */
async function getTournaments() {
  const response = await getZ(tournament_url)

  if (response) {
    return response
  }
  return []
}

async function getTournament() {
  const response = await getZ(tournament_url + '/play')

  if (response) {
    return response
  }
  return []
}

export {
  getTournaments
}