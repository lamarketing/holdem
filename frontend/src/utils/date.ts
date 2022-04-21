function makeDate(date: string) {
  return new Date(date).toLocaleString('ru', {
    weekday: 'long', month: 'long', day: 'numeric',
    hour: "numeric", minute: "numeric",
    timeZone: 'Europe/Moscow'
  })
}

function makeCountDown(date: string) {
  const start = new Date(date)
  const now = new Date()
  // const result = start - now
  // console.log(result)
  return Math.round((start.valueOf() - now.valueOf())/1000)
}

export {
  makeDate,
  makeCountDown
}