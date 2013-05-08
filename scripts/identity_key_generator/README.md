About
-----

This is a crude hack of link:https://github.com/katmagic/Shallot[Shallot] a tool for
generating vanity hidden service address and the corresponding keys. My modifications
simply make the tool generate a 40 byte public key hash instead of the truncated hash
used for onion addresses. Once it has found an identity key digest matching the given
pattern it will output the base32 encoded digest followed by the corrosponding private
key. This private key should then be placed in the Tor data directory as keys/secret_id_key.
When the Tor instance is reload it should have the generate identity digest/fingerprint.

Note: I have a feeling this script has a bug and is not generating correct output everytime.
You should confirm the generated identiy_key from the private key by some other means such
as openssl.

Usage
------------

    $ ./id_key_gen ^tor
    torvo2fumwgmhcxl3d4npjm7r444s5kp
    -----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQDnmBhm2Bv0QMGmV+EqAW87xNpv+dYKJ0TiJ35GdNI0KHGFq++B
    jp0hQagjXy9i7qOrnha6ykSokoSWxDyyVcPAB4fGa65WoWw5UisebGLzG+zNjSVs
    aumwSOTEWI/FgwmA38xy9CG2rx9J2qSvwZLNLaqInkbGLOH1WPJwyQib7wIDAcBb
    AoGAC8ZG3k+Zp8RWeNp4UDBKlyr3tB8d9jWsCE769GphNSgGGgi7Ox/YB2munTcX
    zUM/64EGbsMjnM2hlRhoTf+pNeFHaHR6AK8VvJMzOYFUBSiB7/P8g1T3Tc3MJaTo
    GBQedl3RB8r4Kc/lalVRuAz7ouZ9BiT9XoGJYihlE9sBSecCQQD+gmVfl00AXm/v
    cs4LqAVXG/A5teFAOBL6hvt7U5gEKYQHGrGeLMVnSmA4z+ePj1eURi6MOY2mHtYh
    cAjBSRnjAkEA6PNXRBJGYc3QmKio1DG1vOJ+0brt4OJZu+PlVjyFxWWSRscqg6Cy
    QRTH2ReF99f2NoAicqDSV5UCodwtaCWDhQJAFxL5g2o8NzDJXM+NECnAihNL4ZvL
    28nfLlpSsa7IeR7umjtm058Mw8ZKKIUY9h7bPJYLHKdG2hG5zSi4TxBfNwJBAI+v
    PaOLT6GAjiSl4eEIXl6P7WN6NdsVy03tkoi+vpSzxVeEL0ugxanvMZmM248ZbpQO
    eAok1qU7Umxef96p22MCQQCxEXN810vKjrXlDmXSDHLSBcJZMflrklVkg4PQGVm5
    hAwPyZAWxUUgjKRgS0aZ7O3JxUbFc5vuyMixn2N6VO3+
    -----END RSA PRIVATE KEY-----

