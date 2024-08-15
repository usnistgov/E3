document.addEventListener("DOMContentLoaded", () => {
    tsParticles.load("tsparticles", {
        fpsLimit: 60,
        fullScreen: {
            enable: false
        },
        particles: {
            color: "#000000",
            move: {
                direction: "none",
                enable: true,
                outModes: "out",
                random: false,
                speed: 0.1,
                straight: false
            },
            links: {
                distance: 150,
                color: "#000000",
                enable: true,
                opacity: 0.2
            },
            number: {
                value: 25
            },
            shape: {
                options: {
                    character: {
                        value: "$"
                    }
                },
                type: "char"
            },
            size: {
                value: { min: 5, max: 8 }
            }
        }
    });
});