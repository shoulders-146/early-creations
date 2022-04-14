import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js'
import * as dat from 'lil-gui'
import { Mesh, MeshBasicMaterial,Face3, DoubleSide } from 'three'

/**
 * Base
 */
// Debug
const gui = new dat.GUI()

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

/**
 * Textures  
 */
const textureLoader = new THREE.TextureLoader()
const matcapTexture = textureLoader.load('textures/matcaps/8.png')

/**
 * Fonts
 */
const fontLoader = new FontLoader()


/**
 * Objects
 */
//triangle
//coordinate
const x = -1.1;
const y = 0;
const z = 0.45 * 0.5;

const geom = new THREE.BufferGeometry();
const positionsArray = new Float32Array([
    x + 0, y + 0, z + 0, //0
    x + 1, y + 0, z + 0, //1
    x + 0.5, y + 0.5 * Math.sqrt(3), z + 0, //2

    x + 0, y + 0, z - 0.25, //3
    x + 1, y + 0, z - 0.25, //4
    x + 0.5, y + 0.5 * Math.sqrt(3), z - 0.25,  //5

    x + 0.3, y + 0.18, z + 0, //6
    x + 0.7, y + 0.18, z + 0, //7
    x + 0.5, y + 0.55, z + 0, //8

    x + 0.3, y + 0.18, z - 0.25, //9
    x + 0.7, y + 0.18, z - 0.25, //10
    x + 0.5, y + 0.55, z - 0.25  //11

])
const colorsArray = new Float32Array([
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 1.0, 0.0,
    1.0, 1.0, 0.0,

    0.0, 1.0, 0.0,
    1.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    0.0, 1.0, 1.0,

    0.0, 1.0, 0.0,
    1.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    0.0, 1.0, 1.0,
])

geom.setAttribute( 'position', new THREE.BufferAttribute( positionsArray, 3 ) );
geom.setAttribute( 'color', new THREE.BufferAttribute( colorsArray, 3 ) );
geom.setIndex([
    0, 1, 7,
    7, 0, 6,
    6, 0, 8,
    8, 0, 2,
    2, 8, 7,
    7, 2, 1,
    1, 2, 5,
    5, 1, 4,
    4, 3, 10,
    10, 3, 9,
    9, 3, 11,
    11, 3, 5,
    5, 11, 10,
    10, 5, 4,
    4, 1, 3,
    3, 1, 0,
    0, 2, 3,
    3, 2, 5
])
const triMaterial = new THREE.MeshBasicMaterial( { vertexColors: THREE.VertexColors, side:DoubleSide } );
const gMesh = new THREE.Mesh( geom, triMaterial )
gMesh.position.x -= 1.2
scene.add(gMesh)

//Text
fontLoader.load(
    '/fonts/helvetiker_regular.typeface.json',
    (font) =>
    {
        // Material
        const material = new THREE.MeshMatcapMaterial({ matcap: matcapTexture })

        // Text
        const textGeometry = new TextGeometry(
            'X —> 0',
            {
                font: font,
                size: .8,
                height: 0.2,
                curveSegments: 12,
                bevelEnabled: true,
                bevelThickness: 0.03,
                bevelSize: 0.02,
                bevelOffset: 0,
                bevelSegments: 5
            }
        )
        // textGeometry.center()

        const text = new THREE.Mesh(textGeometry, material)
        gMesh.add(text)

        // Text1
        const textGeometry1 = new TextGeometry(
            'x - sinx ~ x^3 / 6',
            {
                font: font,
                size: .5,
                height: 0.2,
                curveSegments: 12,
                bevelEnabled: true,
                bevelThickness: 0.03,
                bevelSize: 0.02,
                bevelOffset: 0,
                bevelSegments: 5
            }
        )

        const text1 = new THREE.Mesh(textGeometry1, material)
        text1.rotation.x = Math.PI
        text1.position.x -= 1.5
        gMesh.add(text1)
        // textGeometry.center()
        // // Donuts
        // const donutGeometry = new THREE.TorusGeometry(0.3, 0.2, 32, 64)

        // for(let i = 0; i < 100; i++)
        // {
        //     const donut = new THREE.Mesh(donutGeometry, material)
        //     donut.position.x = (Math.random() - 0.5) * 10
        //     donut.position.y = (Math.random() - 0.5) * 10
        //     donut.position.z = (Math.random() - 0.5) * 10
        //     donut.rotation.x = Math.random() * Math.PI
        //     donut.rotation.y = Math.random() * Math.PI
        //     const scale = Math.random()
        //     donut.scale.set(scale, scale, scale)

        //     scene.add(donut)
        // }
    }
)

/**
 * Helper
 */
const axesHelper = new THREE.AxesHelper( 5 );
scene.add( axesHelper );
axesHelper.visible = false

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
camera.position.x = 0
camera.position.y = 0
camera.position.z = 2.6
scene.add(camera)

gui.add(camera.position, 'x').min(-10).max(10).step(0.1).name("x")
gui.add(camera.position, 'y').min(-10).max(10).step(0.1).name("y")
gui.add(camera.position, 'z').min(-10).max(10).step(0.1).name("z")

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Animate
 */
const clock = new THREE.Clock()

const tick = () =>
{
    const elapsedTime = clock.getElapsedTime()

    //animate
    gMesh.rotation.x +=  .02

    // Update controls
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()