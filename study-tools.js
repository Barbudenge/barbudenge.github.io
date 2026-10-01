/* Independent teaching examples in the editorial portal; no application code. */
(() => {
  const pt = document.documentElement.lang.startsWith('pt');
  const number = value => new Intl.NumberFormat(pt ? 'pt-BR' : 'en', {maximumFractionDigits: 3}).format(value);
  const time = value => new Intl.NumberFormat(pt ? 'pt-BR' : 'en', {maximumSignificantDigits: 6}).format(value);
  const message = (br, en) => pt ? br : en;
  const cam = document.querySelector('[data-cam-study]');
  if (cam) {
    cam.hidden = false;
    cam.addEventListener('submit', event => {
      event.preventDefault();
      if (!cam.reportValidity()) return;
      const h = Number(cam.elements.lift.value);
      const beta = Number(cam.elements.angle.value) * Math.PI / 180;
      const rpm = Number(cam.elements.rpm.value);
      const rate = (rpm * 2 * Math.PI / 60) / beta;
      const values = [1 / rate, 2 * h * rate, 1.875 * h * rate,
        2 * Math.PI * h * rate ** 2, (10 * Math.sqrt(3) / 3) * h * rate ** 2,
        4 * Math.PI ** 2 * h * rate ** 3, 60 * h * rate ** 3];
      const output = document.querySelector('[data-cam-result]');
      output.textContent = message('Tempo de subida: ', 'Rise time: ') + time(values[0]) + ' s. ' +
        message('Cicloidal / polinomial 3-4-5: velocidade máxima ', 'Cycloidal / 3-4-5 polynomial: peak velocity ') +
        number(values[1]) + ' / ' + number(values[2]) + ' mm/s; ' +
        message('aceleração máxima em módulo ', 'peak absolute acceleration ') + number(values[3]) + ' / ' + number(values[4]) + ' mm/s²; ' +
        message('jerk no início e no fim da subida ', 'jerk at the start and end of the rise ') + number(values[5]) + ' / ' + number(values[6]) + ' mm/s³. ' +
        message('Na parada, o jerk é zero; a junção continua tendo um salto de jerk nas duas leis.', 'During dwell, jerk is zero; both laws still have a jerk jump at the join.');
    });
  }
  const planet = document.querySelector('[data-planet-study]');
  if (planet) {
    planet.hidden = false;
    planet.addEventListener('submit', event => {
      event.preventDefault();
      if (!planet.reportValidity()) return;
      const ns = Number(planet.elements.sun.value), nr = Number(planet.elements.ring.value);
      const sunSpeed = Number(planet.elements.sunSpeed.value), ringSpeed = Number(planet.elements.ringSpeed.value);
      const output = document.querySelector('[data-planet-result]');
      const satellite = (nr - ns) / 2;
      if (satellite <= 0 || !Number.isInteger(satellite)) {
        output.textContent = message('Geometria incompatível: a coroa deve ter mais dentes que o sol, e a diferença deve ser par. O número de dentes do satélite precisa ser um inteiro positivo.', 'Incompatible geometry: the ring must have more teeth than the sun, and the difference must be even. The planet tooth count must be a positive integer.');
        return;
      }
      const carrier = (ns * sunSpeed + nr * ringSpeed) / (ns + nr);
      output.textContent = message('Braço: ', 'Carrier: ') + number(carrier) + ' rpm. ' +
        message('Satélite: ', 'Planet: ') + satellite + message(' dentes. ', ' teeth. ') +
        message('Sol relativo ao braço: ', 'Sun relative to carrier: ') + number(sunSpeed - carrier) + ' rpm; ' +
        message('coroa relativa ao braço: ', 'ring relative to carrier: ') + number(ringSpeed - carrier) + ' rpm. ' +
        message('A condição de dentes é necessária, mas não verifica interferência nem a montagem de vários satélites.', 'The tooth condition is necessary, but does not check interference or assembly of multiple planets.');
    });
  }
})();
