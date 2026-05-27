export default function EnvironmentStatusCard({
                                                  environmentStatus
                                              }) {

    return (

        <div>

            <h3>
                Environment Status
            </h3>

            <p>
                {environmentStatus}
            </p>

        </div>
    );
}