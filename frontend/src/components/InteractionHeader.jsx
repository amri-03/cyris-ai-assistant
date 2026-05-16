export default function InteractionHeader({
                                              title,
                                              subtitle
                                          }) {

    return (

        <div
            style={{
                marginBottom: "20px"
            }}
        >

            <h1>
                {title}
            </h1>

            <p>
                {subtitle}
            </p>

        </div>
    );
}