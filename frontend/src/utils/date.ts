function makeDate(date: string) {
  return new Date(date).toLocaleString('ru', {
    weekday: 'long', month: 'long', day: 'numeric',
    hour: "numeric", minute: "numeric",
    timeZone: 'Europe/Moscow'
  })
}


export {
  makeDate
}