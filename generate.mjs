function buildJet() {
  return `
<g id="jet">
  <g transform="translate(0,0)">

    <!-- Main body -->
    <polygon
      points="0,-16 8,6 4,3 -4,3 -8,6"
      fill="#58A6FF"
      stroke="#1F6FEB"
      stroke-width="1"
    />

    <!-- Left wing -->
    <polygon
      points="-8,6 -14,12 -4,7"
      fill="#388BFD"
    />

    <!-- Right wing -->
    <polygon
      points="8,6 14,12 4,7"
      fill="#388BFD"
    />

    <!-- Cockpit -->
    <circle
      cx="0"
      cy="-6"
      r="2.2"
      fill="#DDF4FF"
    />

    <!-- Engine flame -->
    <polygon
      points="-3,7 3,7 0,15"
      fill="#F0883E"
    >
      <animate
        attributeName="opacity"
        values="0.5;1;0.6;1"
        dur="0.18s"
        repeatCount="indefinite"
      />
    </polygon>

  </g>

  <animateTransform
    attributeName="transform"
    attributeType="XML"
    type="translate"
    dur="${LOOP_DUR}s"
    repeatCount="indefinite"
    keyTimes="0;0.5;1"
    values="${JET_X_START}.00,140.00;${JET_X_END}.00,140.00;${JET_X_START}.00,140.00"
  />
</g>`;
}
