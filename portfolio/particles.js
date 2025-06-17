window.addEventListener('load', () => {
  const canvas = document.getElementById('bg-canvas');
  const ctx = canvas.getContext('2d');

  let width, height;
  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.1;
      this.vy = (Math.random() - 0.5) * 0.1;
      this.radius = 2;
    }
    move() {
      this.x += this.vx;
      this.y += this.vy;

      if(this.x < 0 || this.x > width) this.vx = -this.vx;
      if(this.y < 0 || this.y > height) this.vy = -this.vy;
    }
    draw() {
      ctx.beginPath();
      ctx.fillStyle = 'purple';
      ctx.shadowColor = 'purple';
      ctx.shadowBlur = 10;
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  const particles = [];
  const PARTICLE_COUNT = 30 ;
  for(let i=0; i<PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  const mouse = {x: null, y: null};
  window.addEventListener('mousemove', e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });
  window.addEventListener('mouseout', () => {
    mouse.x = null;
    mouse.y = null;
  });

  function connectParticles() {
    for(let i=0; i<PARTICLE_COUNT; i++) {
      for(let j=i+1; j<PARTICLE_COUNT; j++) {
        let p1 = particles[i];
        let p2 = particles[j];
        let dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
        if(dist < 120) {
          ctx.strokeStyle = `rgba(255,255,255,${1 - dist/120})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
      if(mouse.x !== null && mouse.y !== null) {
        let p = particles[i];
        let distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
        if(distMouse < 150) {
          ctx.strokeStyle = `rgba(255,255,255,${1 - distMouse/150})`;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();

          p.vx += (mouse.x - p.x) * 0.0005;
          p.vy += (mouse.y - p.y) * 0.0005;
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach(p => {
      p.move();
      p.draw();
    });
    connectParticles();
    requestAnimationFrame(animate);
  }
  animate();
});

