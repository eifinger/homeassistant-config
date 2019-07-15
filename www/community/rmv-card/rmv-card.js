class RmvCard extends HTMLElement {
  set hass (hass) {
    const entityId = this.config.entity
    const state = hass.states[entityId]
    const name = state.attributes['friendly_name']

    if (!this.content) {
      const card = document.createElement('ha-card')
      card.header = name
      this.content = document.createElement('div')
      const style = document.createElement('style')
      style.textContent = `
        table {
          width: 100%;
          padding: 6px 14px;
        }
        td {
          padding: 3px 0px;
        }
        td.shrink {
          white-space:nowrap;
        }
        td.expand {
          width: 99%
        }
        span.line {
          font-weight: bold;
          font-size:0.9em;
          padding:3px 8px 2px 8px;
          color: #fff;
          background-color: #888;
          margin-right:0.7em;
        }
        span.S {
          background-color: #009252;
        }
        span.U-Bahn {
          background-color: #0067ad;
        }
        span.Tram {
          background-color: #eb6810;
        }
        span.Bus {
          background-color: #a3047a;
        }
        span.Bahn {
          background-color: #000000;
        }
        `
      card.appendChild(style)
      card.appendChild(this.content)
      this.appendChild(card)
    }

    var tablehtml = `
    <table>
    `
    const now = new Date()
    const utc = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate(),
      now.getHours(), now.getMinutes(), now.getSeconds(), now.getMilliseconds())
    const next = {
      'line': state.attributes['line'],
      'product': state.attributes['product'],
      'destination': state.attributes['destination'],
      'departure_time': state.attributes['departure_time'],
      'direction': state.attributes['direction']
    }
    const journeys = [next].concat(state.attributes['next_departures'])
    for (const journey of journeys) {
      var destination = journey['destination']
      if (typeof journey['destination'] === 'undefined') {
        destination = journey['direction']
      }
      const linename = journey['line']
      const product = journey['product']

      const jtime = new Date(journey['departure_time'] + 'Z')
      const time = parseInt((jtime.getTime() - utc) / 60000)

      tablehtml += `
          <tr>
            <td class="shrink" style="text-align:center;"><span class="line ${product} ${linename}">${linename}</span></td>
            <td class="expand">${destination}</td>
            <td class="shrink" style="text-align:right;">${time}</td>
          </tr>
      `
    }
    tablehtml += `
    </table>
    `

    this.content.innerHTML = tablehtml
  }

  setConfig (config) {
    if (!config.entity) {
      throw new Error('You need to define an entity')
    }
    this.config = config
  }

  getCardSize () {
    return 1
  }
}

customElements.define('rmv-card', RmvCard)
